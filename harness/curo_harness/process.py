"""Structured process execution with bounded process-tree timeout handling."""

from __future__ import annotations

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from typing import List, Optional


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
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
        return ProcessResult(process.returncode, stdout, stderr, False,
                             round((time.perf_counter() - started) * 1000, 2), None)
    except subprocess.TimeoutExpired as exc:
        partial_stdout = _text(exc.stdout)
        partial_stderr = _text(exc.stderr)
        terminated = False
        termination_error = ""
        try:
            if os.name == "nt":
                killer = subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    capture_output=True, text=True, shell=False, timeout=15,
                )
                terminated = killer.returncode == 0
                if not terminated:
                    termination_error = killer.stderr.strip() or killer.stdout.strip()
                    process.kill()
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
