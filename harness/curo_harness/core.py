"""Core utilities for hashing, time, and filesystem operations."""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union


def utc_now_iso() -> str:
    """Return current UTC timestamp formatted as ISO-8601 with Z suffix."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(data: bytes) -> str:
    """Calculate SHA-256 hash of bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(file_path: Union[str, Path]) -> str:
    """Calculate SHA-256 hash of a file on disk."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found for hashing: {file_path}")
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def sha256_dict(data: Dict[str, Any]) -> str:
    """Calculate deterministic canonical SHA-256 hash of a JSON-serializable dictionary."""
    canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(canonical_json)


def get_curo_root() -> Path:
    """Resolve the E:/curo repository root."""
    # curo_harness is located at E:/curo/harness/curo_harness
    return Path(__file__).resolve().parents[2]


def safe_read_json(file_path: Union[str, Path]) -> Any:
    """Safely read and parse a JSON file."""
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_within(root: Union[str, Path], candidate: Union[str, Path]) -> Path:
    """Resolve *candidate* and require it to remain inside *root*."""
    # Resolve existing symlink/junction components before enforcing authority.
    # A purely lexical check can be bypassed by a junction inside the boundary.
    boundary = Path(os.path.realpath(str(Path(root).resolve())))
    raw = Path(candidate)
    lexical = raw.resolve() if raw.is_absolute() else (boundary / raw).resolve()
    resolved = Path(os.path.realpath(str(lexical)))
    try:
        resolved.relative_to(boundary)
    except (ValueError, OSError) as exc:
        raise ValueError(f"Path escapes authorized boundary '{boundary}': {candidate}") from exc
    return resolved


@contextmanager
def _exclusive_file_lock(target: Path, timeout_seconds: float = 5.0) -> Iterator[None]:
    """Take a bounded same-machine lock for one authoritative target."""
    lock_path = target.with_name(f".{target.name}.lock")
    deadline = time.monotonic() + timeout_seconds
    descriptor: Optional[int] = None
    while descriptor is None:
        try:
            descriptor = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(descriptor, str(os.getpid()).encode("ascii"))
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Timed out acquiring persistence lock: {lock_path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def safe_write_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> None:
    """Atomically write JSON using a bounded per-target local lock."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    with _exclusive_file_lock(path):
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n", dir=str(path.parent),
                prefix=f".{path.name}.", suffix=".tmp", delete=False,
            ) as stream:
                temporary = Path(stream.name)
                json.dump(data, stream, indent=indent)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(str(temporary), str(path))
            temporary = None
        finally:
            if temporary is not None:
                try:
                    temporary.unlink()
                except FileNotFoundError:
                    pass
