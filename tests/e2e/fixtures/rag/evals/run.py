"""Eval harness for the datasheet RAG pipeline (synthetic fixture, deterministic).

Usage: python -m evals.run --set golden

Reads the golden set and the recorded pipeline outputs for the current retriever
configuration, computes retrieval, answer and cost metrics, prints them, and writes
evals/results/latest.json. It never touches the baseline.
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JUDGE_MODEL = "example-judge-v1"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                              cwd=ROOT.parent).stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="golden")
    a = ap.parse_args()
    golden = {g["id"]: g for g in load_jsonl(ROOT / a.set / f"{a.set}.jsonl")}
    from app import retriever
    outputs_path = ROOT / "data" / f"outputs_chunk{retriever.CHUNK_SIZE}.json"
    outputs = json.loads(outputs_path.read_text(encoding="utf-8"))

    hits, rr, faith, lat, cost, failing = [], [], [], [], [], []
    for qid, g in sorted(golden.items()):
        o = outputs[qid]
        retrieved = o["retrieved_ids"][:5]
        expected = set(g["expected_source_ids"])
        hit = any(r in expected for r in retrieved)
        hits.append(1.0 if hit else 0.0)
        rank = next((i + 1 for i, r in enumerate(retrieved) if r in expected), None)
        rr.append(1.0 / rank if rank else 0.0)
        faith.append(o["faithfulness"])
        lat.append(o["latency_ms"])
        cost.append(o["cost_usd"])
        if not hit or o["faithfulness"] < 0.7:
            failing.append(qid)

    lat_sorted = sorted(lat)
    p95 = lat_sorted[min(len(lat_sorted) - 1, int(round(0.95 * (len(lat_sorted) - 1))))]
    result = {
        "commit": commit(),
        "chunk_size": retriever.CHUNK_SIZE,
        "judge_model": JUDGE_MODEL,
        "n": len(golden),
        "recall_at_5": round(statistics.mean(hits), 3),
        "mrr": round(statistics.mean(rr), 3),
        "faithfulness": round(statistics.mean(faith), 3),
        "latency_p50_s": round(statistics.median(lat) / 1000, 2),
        "latency_p95_s": round(p95 / 1000, 2),
        "cost_per_query_usd": round(statistics.mean(cost), 4),
        "failing_ids": failing,
    }
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "latest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"eval set={a.set} n={result['n']} commit={result['commit']} chunk_size={result['chunk_size']} judge={JUDGE_MODEL}")
    for key in ("recall_at_5", "mrr", "faithfulness", "latency_p50_s", "latency_p95_s", "cost_per_query_usd"):
        print(f"{key:20s} {result[key]}")
    print("failing_ids         ", ", ".join(failing) or "none")
    print("raw outputs per question: evals/data/" + outputs_path.name)
    print("results written to evals/results/latest.json")


if __name__ == "__main__":
    main()
