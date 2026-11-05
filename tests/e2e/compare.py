"""Compare skill versions: baseline run dir (both arms, old skills) vs a later with-skill run dir.

  python tests/e2e/compare.py BASELINE_DIR AFTER_DIR > compare.md

Per skill and per scenario: without-skill (baseline dir), with old skill (baseline dir), with new
skill (after dir). Score = passed assertions / all assertions (objective checks + rubric).
"""
from __future__ import annotations

import glob
import json
import os
import statistics
import sys
from collections import defaultdict


def load(d: str) -> list[dict]:
    out = []
    for f in sorted(glob.glob(os.path.join(d, "runs", "*.json"))):
        r = json.load(open(f, encoding="utf-8"))
        if "error" not in r:
            out.append(r)
    return out


def agg(rs: list[dict]) -> tuple[str, float, float, int]:
    if not rs:
        return "-", 0.0, 0.0, 0
    p = sum(r["checks_passed"] + r["rubric_passed"] for r in rs)
    t = sum(r["checks_total"] + r["rubric_total"] for r in rs)
    return (f"{p}/{t} ({p / t:.0%})", statistics.mean(r["cost_usd"] for r in rs),
            statistics.mean(sum(r["tokens"].values()) for r in rs), len(rs))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252
    base, after = load(sys.argv[1]), load(sys.argv[2])
    cells = defaultdict(list)
    for r in base:
        cells[(r["skill"], r["scenario"], "without" if r["arm"] == "without" else "old")].append(r)
    for r in after:
        if r["arm"] == "with":
            cells[(r["skill"], r["scenario"], "new")].append(r)
    skills = sorted({k[0] for k in cells if k[0]})
    print("| Skill | Without skill | With skill (before fixes) | With skill (after fixes) | Tokens/run without → after | Cost/run without → after |")
    print("|---|---|---|---|---|---|")
    for sk in skills:
        row = {arm: [r for (s, _, a), rs in cells.items() if s == sk and a == arm for r in rs] for arm in ("without", "old", "new")}
        w, o, n = agg(row["without"]), agg(row["old"]), agg(row["new"])
        print(f"| {sk} | {w[0]} | {o[0]} | {n[0]} | {int(w[2]):,} → {int(n[2]):,} | ${w[1]:.3f} → ${n[1]:.3f} |")
    print()
    print("| Scenario | Without skill | Before fixes | After fixes |")
    print("|---|---|---|---|")
    for sid in sorted({k[1] for k in cells if k[0]}):
        sk = next(k[0] for k in cells if k[1] == sid)
        print(f"| {sid} | {agg(cells[(sk, sid, 'without')])[0]} | {agg(cells[(sk, sid, 'old')])[0]} | {agg(cells[(sk, sid, 'new')])[0]} |")


if __name__ == "__main__":
    main()
