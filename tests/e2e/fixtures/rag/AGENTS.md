# AGENTS.md

## Project
Quotes assistant: answers questions about product datasheets with retrieval-augmented generation.

## Stack
- Python 3.11, pytest
- Run tests: `python -m pytest -q`

## Evaluation harness
- EVAL_CMD: `python -m evals.run --set golden`
- BASELINE: `evals/baselines/main.json`
- Golden set: `evals/golden/golden.jsonl`
- Judge model for faithfulness: recorded in the harness output.

## Don't
- Don't change the eval baseline without asking.
