# PreCompact backup hook (infrastructure, not a skill)

Saves the full transcript to `~/.claude/transcript-backups/` every time Claude Code compacts, so nothing is lost if the summary drops a constraint. Keeps the newest 50.

1. Copy `precompact_backup.py` to `~/.claude/hooks/`.
2. Add to `~/.claude/settings.json` (merge with any existing `hooks` key):

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": "python3 ~/.claude/hooks/precompact_backup.py" }
        ]
      }
    ]
  }
}
```

On Windows use `python "%USERPROFILE%\\.claude\\hooks\\precompact_backup.py"` as the command.

Verify: run `/compact` in a test session and check the backups folder.
Transcripts can contain secrets from your sessions — keep this folder private.
