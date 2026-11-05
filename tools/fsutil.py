"""Filesystem helpers shared by the library's tools. Stdlib only."""
from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path


def _clear_readonly_and_retry(func, path, _exc) -> None:
    # Git writes its object files read-only; on Windows os.unlink refuses read-only files.
    os.chmod(path, stat.S_IWRITE)
    func(path)


def rmtree(path: str | Path) -> None:
    """shutil.rmtree that also removes read-only files (e.g. a .git directory on Windows)."""
    if not Path(path).exists():
        return
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_clear_readonly_and_retry)
    else:
        shutil.rmtree(path, onerror=_clear_readonly_and_retry)
