---
name: context-continuity-check
description: Use after writing a handoff, before clearing or compacting context, or at the start of a session resumed from a handoff — verifies constraints, source references, pending work and test status are recoverable.
---

# Context Continuity Check

**Status: DRAFT.** Test with `evals/evals.json` via skill-creator.

## Three different jobs — don't merge them
| Action | Job |
|---|---|
| `handoff` skill (manual) | Move work to a NEW session via a Markdown handoff doc |
| native `/compact` | Continue in the SAME session with summarized history |
| this skill | Verify the transferred state is complete and accurate |

The real test is a fresh session with no access to the old chat — only the handoff + repo. Asking the original agent "is your summary complete?" is not a test.

## When to use
- Right after `handoff` produces a document
- Before `/clear` or compaction on a long task
- First step of a fresh session that starts from a handoff
- NOT for: short tasks that finish in one session

## Procedure
1. **Locate artifacts**: handoff doc, AGENTS.md / CLAUDE.md, open spec (OpenSpec change), latest test output, git status.
2. **Checklist — each must be present and specific:**
   - [ ] Goal of the current task in one sentence
   - [ ] Approved constraints and decisions (with where they were decided — ADR / spec / chat)
   - [ ] Exact file paths and source references (doc + clause), not paraphrases
   - [ ] What is done, with evidence (commit hash, test command + result)
   - [ ] What is pending, in order, with the very next action
   - [ ] Known failures / open questions
   - [ ] Branch / worktree name
3. **Verify against the repo**: run `git log -5`, `git status`, and the test command named in the handoff. Mismatch → flag it.
4. **Reconstruction test** (resume case): state the next task in your own words from the handoff alone, then confirm against repo evidence.
5. Report missing / stale items and patch the handoff.

## Success condition
A fresh session correctly states the next task and its constraints from the handoff plus repository evidence, with no question the handoff should have answered.
