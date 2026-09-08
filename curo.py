#!/usr/bin/env python3
"""Root CLI entrypoint for Curo Harness."""
import sys
from pathlib import Path

# Add harness directory to sys.path
harness_dir = Path(__file__).resolve().parent / "harness"
if str(harness_dir) not in sys.path:
    sys.path.insert(0, str(harness_dir))

from curo_harness.cli import main

if __name__ == "__main__":
    sys.exit(main())
