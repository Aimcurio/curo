"""Deterministic safety helpers for telemetry and legacy command input."""

from __future__ import annotations

import os
import re
import shlex
from typing import List, Tuple


_REDACTIONS = (
    (re.compile(r"(?im)(authorization\s*:\s*(?:bearer|basic)\s+)[^\s]+"), r"\1[REDACTED]"),
    (re.compile(r"(?im)\b(api[_-]?key|access[_-]?token|secret|password)\b(\s*[:=]\s*)[^\s,;]+"), r"\1\2[REDACTED]"),
    (re.compile(r"(?im)\b(OPENAI_API_KEY|AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|NPM_TOKEN)\s*=\s*[^\s]+"), r"\1=[REDACTED]"),
    (re.compile(r"\b(sk-(?:proj-)?[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9_]{8,}|AKIA[0-9A-Z]{12,})\b"), "[REDACTED]"),
    (re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.DOTALL), "[REDACTED PRIVATE KEY]"),
)


def redact_secrets(text: str) -> Tuple[str, bool]:
    """Conservatively scrub common secret forms; this is not exhaustive detection."""
    scrubbed = text
    for pattern, replacement in _REDACTIONS:
        scrubbed = pattern.sub(replacement, scrubbed)
    return scrubbed, scrubbed != text


def parse_legacy_command(command: str) -> Tuple[str, List[str]]:
    """Convert a deprecated simple command string, rejecting shell syntax."""
    if not command.strip():
        raise ValueError("Legacy command string is empty")
    if re.search(r"(?:&&|\|\||[|;<>&`]|\$\(|\r|\n)", command):
        raise ValueError("Legacy command contains prohibited shell syntax; use executable and args")
    parts = shlex.split(command, posix=os.name != "nt")
    if not parts:
        raise ValueError("Legacy command string is empty")
    return parts[0], parts[1:]
