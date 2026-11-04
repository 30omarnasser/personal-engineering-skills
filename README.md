# Personal Engineering Skill Library

A portable set of agent skills for Python / FastAPI / document-intelligence / multi-agent work.
Drop it on any machine, run one command for the global set, one more per project.
21 skills installed by default, 2 optional. Every skill loads only when its job comes up.

## Quick start

```bash
git clone <your-repo> ~/skills-library && cd ~/skills-library
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
02-planning-architecture/   GLOBAL   grill-with-docs* · domain-modeling · ask-matt*
03-review-workflow/         GLOBAL   requesting-code-review · using-git-worktrees
04-security-correctness/    PROJECT  security-model · supply-chain-risk-auditor · find-bugs ·
                                     spec-to-code-compliance · property-based-testing
05-ai-engineering/          PROJECT  huggingface-local-models
06-custom-domain/           PROJECT  procurement-evidence-review · rag-evaluation · context-continuity-check
07-skill-development/       GLOBAL   skill-creator
_optional/                  —        huggingface-best · huggingface-community-evals  (model benchmarking; copy in if needed)
_infra/precompact-backup/   hook     saves full transcript before compaction
templates/AGENTS.md                  starter project file: stack, commands, which skill when
tools/install.py, tools/update.py
manifest.yaml                        source, commit, license, scope, activation, last_evaluated per skill
_licenses/
```
`*` = manual: Claude won't pick these itself; invoke `/handoff`, `/grill-with-docs`, `/ask-matt`.

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

## Testing — the part that actually matters
Nothing here has been evaluated yet (`last_evaluated: null` throughout). Order:
1. The three custom skills. Each has `evals/evals.json` (2 should-trigger, 1 should-not). Run with `skill-creator`, baseline vs with-skill. `context-continuity-check` must be tested from a **fresh session** with only the handoff and repo.
2. Three real tasks — a feature, a hard bug, an AI eval. Note which skills activated, whether they should have, tokens, and unnecessary questions.
3. Remove anything that duplicates another skill or slows work without improving it. Record in `manifest.yaml`.

## Notes
- Skills are copied, not symlinked, so a project keeps working when cloned elsewhere. `update.py` is how you resync.
- If you install the Superpowers or Matt Pocock plugins later, delete the copied versions of their skills — don't run both.
- Several skills ship scripts (`skill-creator`, `security-model`, `supply-chain-risk-auditor`, `modern-python`, `systematic-debugging`). I checked which hosts they contact (public registries, OSV, deps.dev, GitHub, Hugging Face Hub). Read a script before running it anyway.
- `supply-chain-risk-auditor` needs `gh auth login` and reads `uv.lock` (not `poetry.lock`).
- `ask-matt` references Matt skills not installed here; treat its suggestions as hints.

## Licenses
MIT (Superpowers, Matt Pocock) · Apache-2.0 (Hugging Face, Sentry, Anthropic skill-creator) · CC BY-SA 4.0 (Trail of Bits: share-alike if you redistribute modified versions). Copies in `_licenses/`.
