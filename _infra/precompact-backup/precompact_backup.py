#!/usr/bin/env python3
"""Claude Code PreCompact hook: copy the full transcript before it is compacted.

Reads the hook's JSON from stdin, copies transcript_path to
~/.claude/transcript-backups/<session>_<timestamp>.jsonl and keeps the newest 50.
Never blocks compaction: always exits 0.
"""
import json, shutil, sys, time
from pathlib import Path

try:
    data = json.load(sys.stdin)
    src = Path(data.get("transcript_path", "")).expanduser()
    if src.is_file():
        dest_dir = Path.home() / ".claude" / "transcript-backups"
        dest_dir.mkdir(parents=True, exist_ok=True)
        sid = data.get("session_id", "session")[:12]
        trig = data.get("trigger", "auto")
        shutil.copy2(src, dest_dir / f"{sid}_{time.strftime('%Y%m%d-%H%M%S')}_{trig}.jsonl")
        for old in sorted(dest_dir.glob("*.jsonl"), key=lambda f: f.stat().st_mtime)[:-50]:
            old.unlink()
except Exception as e:  # never break compaction
    print(f"precompact backup skipped: {e}", file=sys.stderr)
sys.exit(0)
