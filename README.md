# Personal Engineering Skill Library

A portable set of agent skills for Python / FastAPI / document-intelligence / multi-agent work.
Drop it on any machine, run one command for the global set, one more per project.
21 skills installed by default, 3 optional. Every skill loads only when its job comes up.
Audited and tested 2026-11-04 — see [EVALUATION_REPORT.md](EVALUATION_REPORT.md).

## Quick start

```bash
git clone <your-repo> ~/skills-library && cd ~/skills-library
python tools/check_library.py           # static checks: frontmatter, links, manifest, encoding
python tools/install.py global          # 12 skills -> ~/.claude/skills
python tools/install.py hook            # transcript backup before every /compact
cd /path/to/some/project
python ~/skills-library/tools/install.py project .   # pick the project skills; adds AGENTS.md if missing
```
Windows: same commands with `python`; paths with `$HOME\skills-library`.
Other agents (Codex, Cursor…): add `--dest <their skills folder>`.

Later: `python tools/update.py` shows what changed upstream; `--show` prints SKILL.md diffs; `--apply` takes them.

## Layout

```
01-core-engineering/        GLOBAL   systematic-debugging · verification-before-completion ·
                                     test-driven-development · modern-python · research · handoff*
02-planning-architecture/   GLOBAL   grill-with-docs* · grilling · domain-modeling · ask-matt*
03-review-workflow/         GLOBAL   requesting-code-review · using-git-worktrees
04-security-correctness/    PROJECT  security-model · supply-chain-risk-auditor · find-bugs ·
                                     spec-to-code-compliance · property-based-testing
05-ai-engineering/          PROJECT  huggingface-local-models
06-custom-domain/           PROJECT  procurement-evidence-review · rag-evaluation · context-continuity-check
_optional/                  —        huggingface-best · huggingface-community-evals  (model benchmarking; copy in if needed)
                                     skill-creator  (Claude Code already has it as anthropic-skills:skill-creator)
_infra/precompact-backup/   hook     saves full transcript before compaction
templates/AGENTS.md                  starter project file: stack, commands, which skill when
tools/install.py, tools/update.py, tools/check_library.py, tools/activation_eval.py, tools/e2e_eval.py
tests/                               checker mutation tests, activation cases, e2e scenarios + synthetic fixtures, results
manifest.yaml                        source, commit, license, scope, activation, local_patches, last_evaluated per skill
EVALUATION_REPORT.md                 audit + test results, per-skill scores, remaining risks
_licenses/
```
`*` = manual: Claude won't pick these itself; invoke `/handoff`, `/grill-with-docs`, `/ask-matt`.
`grill-with-docs` dispatches `grilling` + `domain-modeling`; all three install together.

## One owner per job

| Job | Owner | Not also |
|---|---|---|
| Clarify a request | `grill-with-docs` | Superpowers `brainstorming` |
| Spec / plan | OpenSpec (separate tool) | Superpowers `writing-plans`, Matt `to-spec` |
| Write code | `test-driven-development` | Matt `tdd` |
| Debug | `systematic-debugging` | Matt `diagnosing-bugs` |
| Claim done | `verification-before-completion` | — |
| General review | `requesting-code-review` | Matt `code-review`, Sentry `code-review` |
| Security pass on a branch | `find-bugs` | — (second pass, after general review) |
| Dependencies | `supply-chain-risk-auditor` | — |
| Threat model | `security-model` → `SECURITY_MODEL.md` | — |
| Python project setup | `modern-python` | — |
| Evaluate the app | `rag-evaluation` | `huggingface-community-evals` (models only) |
| Leave a session | `/handoff` → `context-continuity-check` | native `/compact` (same session only) |

Worked example — "add authentication to the FastAPI app":
`/grill-with-docs` → OpenSpec spec → `security-model` → `test-driven-development` → `verification-before-completion` → `requesting-code-review` → `find-bugs` → `/handoff`.

## Per-project setup (5 minutes)
1. `python ~/skills-library/tools/install.py project .` and pick what the project needs. Typical FastAPI + RAG service: `security-model`, `supply-chain-risk-auditor`, `find-bugs`, `rag-evaluation`, `context-continuity-check`.
2. Edit the TODOs in `AGENTS.md` — especially `EVAL_CMD` and `BASELINE`, or `rag-evaluation` has nothing to run.
3. Run `security-model` once to create `SECURITY_MODEL.md`; add the LLM threats it doesn't know about: prompt injection through uploaded documents, which tools agents may call, what leaves to external models.

## Testing
Four layers, all run on 2026-11-04/05 (details and numbers in `EVALUATION_REPORT.md`):
1. **Static** — `python tools/check_library.py [--scripts]`: frontmatter, name/dir match, links, manifest ↔ filesystem ↔ `update.py` consistency, UTF-8/LF/hidden characters, script compilation; `--scripts` also runs the vendored pytest suites (security-model resolver, supply-chain collector) and `tests/test_check_library.py`, which seeds defects to prove the checker catches them. Run it before committing and after `update.py --apply`. Free, offline.
2. **Activation** — `python tools/activation_eval.py tests/activation_cases.json out.json --repeat 2` builds a scratch project with every skill plus a small FastAPI fixture and runs each prompt through `claude -p`, scoring which skill fires. 48 cases: a positive and a near-miss negative per skill, the custom skills' `evals/evals.json` prompts, conflict probes, and the three manual skills. Costs real tokens (about $0.35 per prompt). Results from this audit are in `tests/activation-results-2026-11-04/`. For one skill's description, `_optional/skill-creator/scripts/run_eval.py` also works on Windows after the local patch.
3. **End to end** - `python tools/e2e_eval.py OUT_DIR --repeat 2` runs 18 scenarios (`tests/e2e/scenarios.py`) for the three custom skills and three cross-skill chains in locked-down sandboxes built from synthetic fixtures: restricted tools, deny-by-default permissions, no MCP servers, no user settings. Planted prompt injections use canary files and `.invalid` hosts. Each scenario runs with and without the skill; objective checks plus a rubric graded by a separate tool-less model call against fixed ground truth. About $11 per full run. `tests/e2e/report.py` and `compare.py` turn run folders into tables; `tests/test_e2e_fixtures.py` checks every fixture offline.
4. **Real tasks** — still to do by you: a feature, a hard bug, an AI eval. Note which skills activated, whether they should have, tokens, and unnecessary questions. `context-continuity-check` must be tested from a **fresh session** with only the handoff and repo.

Re-test after every `update.py --apply`: upstream description changes alter triggering, and the apply overwrites the local patches listed in `manifest.yaml`.

Both model-driven harnesses refuse to score a run that never reached the model (usage limit, crash, timeout): it is reported as an error and the exit code is 2. Re-run those cases; an errored run says nothing about a skill.

## Notes
- Skills are copied, not symlinked, so a project keeps working when cloned elsewhere. `update.py` is how you resync.
- If you install the Superpowers or Matt Pocock plugins later, delete the copied versions of their skills — don't run both.
- Claude Code ships its own `code-review`, `security-review` and (via the `anthropic-skills` plugin) `skill-creator`. In tests, a generic "review my branch" went to the built-in `code-review` and "security sweep" to the built-in `security-review`; `requesting-code-review` and `find-bugs` trigger on their specific phrasing. If you want the library's versions every time, invoke them by name (`/requesting-code-review`, `/find-bugs`) or disable the built-ins.
- `skill-creator` lives in `_optional/` and is not installed: Claude Code already provides the newer, account-synced `anthropic-skills:skill-creator`. The library copy keeps the Windows fixes to its scripts. On Windows, run description optimization from it directly (`cd _optional/skill-creator && python -m scripts.run_eval ...`), because the synced copy's `run_eval.py` still uses POSIX-only `select()` and passes the query as an argument. Install it (`--dest`) only for agents that lack skill-creator.
- Several upstream files carry local patches (Windows encoding/compat fixes, sharpened descriptions, a standalone fallback for `spec-to-code-compliance`). They are listed per skill under `local_patches` in `manifest.yaml`; `update.py` warns before `--apply` overwrites them.
- Windows: scripts run with `python` (no `uv` needed; they are stdlib-only). `update.py` clones with `core.autocrlf=false` so byte-identical upstream files don't show as changed.
- Several skills ship scripts (`skill-creator`, `security-model`, `supply-chain-risk-auditor`, `modern-python`, `systematic-debugging`). I checked which hosts they contact (public registries, OSV, deps.dev, GitHub, Hugging Face Hub). Read a script before running it anyway.
- `supply-chain-risk-auditor` needs `gh auth login` and reads `uv.lock` (not `poetry.lock`).
- `ask-matt` references Matt skills not installed here; a note at the top of its SKILL.md maps each to the library's owner or marks it "not installed".
- `spec-to-code-compliance` upstream is a plugin (workflow script + agent); the copy here carries a standalone fallback that reproduces the per-requirement fan-out with ordinary subagents and ships the agent prompt in `agents/spec-compliance-checker.md`. Install the Trail of Bits plugin for the full workflow.

## Licenses
MIT (Superpowers, Matt Pocock) · Apache-2.0 (Hugging Face, Sentry, Anthropic skill-creator) · CC BY-SA 4.0 (Trail of Bits: share-alike if you redistribute modified versions). Copies in `_licenses/`.
