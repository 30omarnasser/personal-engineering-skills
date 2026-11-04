# AGENTS.md

<!-- Starter template from personal-engineering-skills. Keep it under ~80 lines; agents read this on every request. Replace every TODO. -->

## Project
TODO: one paragraph — what this service does, who uses it, what "done" means here.

## Stack
- Python 3.12, uv, FastAPI, pytest  <!-- TODO adjust -->
- Run tests: `uv run pytest -q`
- Lint/format: `uv run ruff check . && uv run ruff format .`
- Dev server: `uv run fastapi dev app/main.py`

## Workflow — which skill when
One owner per job. Do not run two planners or two clarifiers on the same task.

| Situation | Do this |
|---|---|
| New feature or unclear request | Ask me to run `/grill-with-docs` first; then spec in OpenSpec (if present). Don't brainstorm separately. |
| Writing code | `test-driven-development`: failing test → code → refactor |
| Bug, failing test, weird output | `systematic-debugging` before any fix |
| About to say "done" / "fixed" | `verification-before-completion` — show the test output |
| Before PR | `requesting-code-review`, then `find-bugs` for a security pass |
| Dependency added or bumped | `supply-chain-risk-auditor` |
| Auth, permissions, untrusted input, external services touched | Read/update `SECURITY_MODEL.md` (`security-model`) |
| Parsers, validators, precedence/exception rules | `property-based-testing` |
| Retrieval / prompt / model change | `rag-evaluation` — numbers from the harness, not opinions |
| Tender or procurement output going to a customer | `procurement-evidence-review` |
| Ending a session or switching agent | `/handoff`, then `context-continuity-check` |

## Evaluation harness  <!-- TODO: required by rag-evaluation -->
- EVAL_CMD: `uv run python -m evals.run --set golden`
- BASELINE: `evals/baselines/main.json`
- Golden set: `evals/golden/*.jsonl`

## Conventions
- Branch per task; use a worktree for anything parallel.
- Commits: imperative, one logical change.
- Never commit secrets; `.env` is gitignored.
- Arabic/RTL and Egyptian units/standards are first-class — don't assume en-US defaults.  <!-- TODO keep or remove -->

## Don't
- Don't claim tests pass without pasting the command and result.
- Don't change the eval baseline without asking.
- Don't install new dependencies without saying why.
