# AGENTS.md

## Project
Quotes service: builds customer quotes and exports them. Arabic (RTL) quotes are first-class.

## Stack
- Python 3.11, pytest
- Run tests: `python -m pytest -q`

## Conventions
- Decisions that are hard to reverse go in `docs/adr/`.
- Never commit secrets; `.env` is gitignored.
