"""Entry point for Vercel serverless deployment."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project package is importable when running on Vercel.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
root_str = str(PROJECT_ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

from proj.app import app  # noqa: E402

# Vercel detects either an "app" or "handler" export. Flask apps are WSGI
# callables, so we can expose both for clarity.
handler = app
