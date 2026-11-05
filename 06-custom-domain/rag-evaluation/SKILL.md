---
name: rag-evaluation
description: Use when a retrieval, chunking, embedding, reranking, prompt or model change is made to a RAG / GraphRAG pipeline, when the user shares eval numbers (recall@k, faithfulness, latency, cost, failing IDs) and asks whether to merge, or before claiming answer quality improved. Runs the project's eval harness against the saved baseline and reports quality, latency and cost with regressions inspected - never estimates numbers. Not for explaining retrieval concepts.
---

# RAG Evaluation

**Status: DRAFT — wire the commands below to your project's actual harness.**

## When to use
- Any change to retrieval, chunking, embeddings, reranking, graph construction, prompts or model
- Before saying "answers are better"
- NOT for: one-off manual Q&A, unrelated code changes

## Prerequisites (per project, record in AGENTS.md)
- `EVAL_CMD` — command that runs the harness, e.g. `uv run python -m evals.run --set golden`
- `BASELINE` — path to saved baseline results, e.g. `evals/baselines/main.json`
- Golden set with question, expected answer / expected source IDs

## Procedure
1. Confirm the golden set and baseline exist. If not, stop and say so — do not invent a baseline.
2. Run `EVAL_CMD` on the current branch. Save raw results with commit hash + timestamp.
3. Compare to `BASELINE` on:
   - Retrieval: recall@k, MRR / hit rate on expected source IDs
   - Answer: correctness / faithfulness (judge model named explicitly), citation accuracy
   - Latency p50 / p95, tokens and cost per query
4. List every case that **regressed** and every case that still **fails**. Open at least 3 and inspect retrieved chunks vs. answer.
5. Classify failures: retrieval miss / ranking / context overflow / generation / grading error.
6. Report.

## Output format
- Metric table: baseline vs. current vs. delta
- Regressions (IDs + one-line cause)
- Verdict: `IMPROVED`, `NO CHANGE`, `REGRESSED`, `MIXED` with the trade-off stated

## Rules
- Numbers come from the harness output only — never estimated.
- An LLM judge's score is not evidence alone; show sample failing cases.
- Update the baseline only when the user approves.

## Success condition
Reproducible results tied to a commit, with regressions inspected — not a subjective claim that answers look better.
