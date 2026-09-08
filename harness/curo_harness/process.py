"""Structured process execution with bounded process-tree timeout handling."""

from __future__ import annotations

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from typing import List, Optional


if os.name == "nt":
    import ctypes
    from ctypes import wintypes

    class _JobObjectBasicLimitInformation(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class _IoCounters(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        ]

    class _JobObjectExtendedLimitInformation(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _JobObjectBasicLimitInformation),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    class _WindowsJob:
        """Own a Windows process tree and kill every member when closed."""

        _KILL_ON_JOB_CLOSE = 0x00002000
        _EXTENDED_LIMIT_INFORMATION = 9

        def __init__(self) -> None:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
            kernel32.CreateJobObjectW.restype = wintypes.HANDLE
            kernel32.SetInformationJobObject.argtypes = (
                wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
            )
            kernel32.SetInformationJobObject.restype = wintypes.BOOL
            kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
            kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
            kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
            kernel32.CloseHandle.restype = wintypes.BOOL
            self._kernel32 = kernel32
            self._handle = kernel32.CreateJobObjectW(None, None)
            if not self._handle:
                raise OSError(ctypes.get_last_error(), "CreateJobObjectW failed")
            limits = _JobObjectExtendedLimitInformation()
            limits.BasicLimitInformation.LimitFlags = self._KILL_ON_JOB_CLOSE
            configured = kernel32.SetInformationJobObject(
                self._handle,
                self._EXTENDED_LIMIT_INFORMATION,
                ctypes.byref(limits),
                ctypes.sizeof(limits),
            )
            if not configured:
                error = ctypes.get_last_error()
                kernel32.CloseHandle(self._handle)
                self._handle = None
                raise OSError(error, "SetInformationJobObject failed")

        def assign(self, process: subprocess.Popen[str]) -> None:
            process_handle = wintypes.HANDLE(int(process._handle))  # type: ignore[attr-defined]
            if not self._kernel32.AssignProcessToJobObject(self._handle, process_handle):
                raise OSError(ctypes.get_last_error(), "AssignProcessToJobObject failed")

        def close(self) -> None:
            if self._handle is not None:
                if not self._kernel32.CloseHandle(self._handle):
                    raise OSError(ctypes.get_last_error(), "CloseHandle(job) failed")
                self._handle = None


@dataclass
class ProcessResult:
    exit_code: Optional[int]
    stdout: str
    stderr: str
    timed_out: bool
    duration_ms: float
    timeout_termination_succeeded: Optional[bool]


def _text(value: object) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value if isinstance(value, str) else ""


def run_structured_process(executable: str, args: List[str], cwd: str, timeout_seconds: float) -> ProcessResult:
    """Run argv without a shell and terminate the created process group on timeout."""
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    started = time.perf_counter()
    windows_job = None
    job_error = ""
    if os.name == "nt":
        try:
            windows_job = _WindowsJob()
        except Exception as exc:
            job_error = str(exc)
    process = subprocess.Popen(
        [executable, *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
        creationflags=creationflags,
        start_new_session=os.name != "nt",
    )
    if windows_job is not None:
        try:
            windows_job.assign(process)
        except Exception as exc:
            job_error = str(exc)
            try:
                windows_job.close()
            except Exception:
                pass
            windows_job = None
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
        if windows_job is not None:
            windows_job.close()
        return ProcessResult(process.returncode, stdout, stderr, False,
                             round((time.perf_counter() - started) * 1000, 2), None)
    except subprocess.TimeoutExpired as exc:
        partial_stdout = _text(exc.stdout)
        partial_stderr = _text(exc.stderr)
        terminated = False
        termination_error = ""
        try:
            if os.name == "nt":
                if windows_job is not None:
                    windows_job.close()
                    windows_job = None
                    terminated = True
                else:
                    killer = subprocess.run(
                        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                        capture_output=True, text=True, shell=False, timeout=15,
                    )
                    terminated = killer.returncode == 0
                    if not terminated:
                        termination_error = killer.stderr.strip() or killer.stdout.strip()
                        process.kill()
                    if job_error:
                        termination_error = f"job object unavailable: {job_error}; {termination_error}".strip("; ")
            else:
                os.killpg(process.pid, signal.SIGKILL)
                terminated = True
        except Exception as kill_exc:
            termination_error = str(kill_exc)
            try:
                process.kill()
            except Exception:
                pass
        try:
            tail_stdout, tail_stderr = process.communicate(timeout=15)
            partial_stdout += tail_stdout or ""
            partial_stderr += tail_stderr or ""
        except Exception as communicate_exc:
            termination_error = termination_error or str(communicate_exc)
        message = f"Execution timed out after {timeout_seconds} seconds"
        if not terminated:
            message += f"; process-tree termination could not be confirmed: {termination_error or 'unknown error'}"
        partial_stderr = f"{partial_stderr}\n{message}".strip()
        return ProcessResult(124, partial_stdout, partial_stderr, True,
                             round((time.perf_counter() - started) * 1000, 2), terminated)
