"""Render e2e results (one or more tools/e2e_eval.py output dirs) as Markdown tables.

  python tests/e2e/report.py RESULTS_DIR [RESULTS_DIR ...] > results.md

Per scenario and arm: mean score, objective checks, rubric, trigger rate, denied tool calls,
cost, total tokens and turns. Per skill: with-skill minus without-skill deltas. Interop:
skills observed per run and failed checks. Every number is computed from the run files.
"""
from __future__ import annotations

import glob
import json
import os
import statistics
import sys
from collections import defaultdict


def load(dirs: list[str]) -> list[dict]:
    runs = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, "runs", "*.json"))):
            r = json.load(open(f, encoding="utf-8"))
            if "error" not in r:
                runs.append(r)
    return runs


def tok(r: dict) -> int:
    return sum(r["tokens"].values())


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252
    runs = load(sys.argv[1:])
    by = defaultdict(list)
    for r in runs:
        by[(r["scenario"], r["arm"])].append(r)
    print("| Scenario | Arm | Runs | Score | Checks | Rubric | Triggered | Denied calls | Cost/run | Tokens/run | Output tok/run | Turns/run |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for (sid, arm), rs in sorted(by.items()):
        trig = f"{sum(1 for r in rs if r['skill_triggered'])}/{len(rs)}" if rs[0]["skill"] else "n/a"
        print(f"| {sid} | {arm} | {len(rs)} | {statistics.mean(r['score'] for r in rs):.2f} | "
              f"{sum(r['checks_passed'] for r in rs)}/{sum(r['checks_total'] for r in rs)} | "
              f"{sum(r['rubric_passed'] for r in rs)}/{sum(r['rubric_total'] for r in rs)} | {trig} | "
              f"{sum(len(r['denials']) for r in rs)} | ${statistics.mean(r['cost_usd'] for r in rs):.3f} | "
              f"{int(statistics.mean(tok(r) for r in rs)):,} | {int(statistics.mean(r['tokens']['output'] for r in rs)):,} | "
              f"{statistics.mean(r['turns'] for r in rs):.1f} |")
    print()
    skills = defaultdict(lambda: defaultdict(list))
    for r in runs:
        if r["skill"]:
            skills[r["skill"]][r["arm"]].append(r)
    print("| Skill | Runs (with/without) | Score with | Score without | Delta | Assertions with | Assertions without | Trigger rate | Cost with | Cost without | Tokens with | Tokens without |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for sk, arms in sorted(skills.items()):
        w, wo = arms.get("with", []), arms.get("without", [])
        if not w or not wo:
            continue
        aw = sum(r["checks_passed"] + r["rubric_passed"] for r in w), sum(r["checks_total"] + r["rubric_total"] for r in w)
        awo = sum(r["checks_passed"] + r["rubric_passed"] for r in wo), sum(r["checks_total"] + r["rubric_total"] for r in wo)
        sw, swo = statistics.mean(r["score"] for r in w), statistics.mean(r["score"] for r in wo)
        print(f"| {sk} | {len(w)}/{len(wo)} | {sw:.3f} | {swo:.3f} | {sw - swo:+.3f} | {aw[0]}/{aw[1]} | {awo[0]}/{awo[1]} | "
              f"{sum(1 for r in w if r['skill_triggered'])}/{len(w)} | ${statistics.mean(r['cost_usd'] for r in w):.3f} | "
              f"${statistics.mean(r['cost_usd'] for r in wo):.3f} | {int(statistics.mean(tok(r) for r in w)):,} | "
              f"{int(statistics.mean(tok(r) for r in wo)):,} |")
    print()
    inter = [r for r in runs if r["kind"] == "interop"]
    if inter:
        print("| Interop run | Score | Skills invoked (in order) | Failed checks / rubric |")
        print("|---|---|---|---|")
        for r in sorted(inter, key=lambda r: (r["scenario"], r["rep"])):
            fails = [c["desc"] for c in r["checks"] if not c["passed"]] + [g["assertion"][:60] for g in r["rubric"] if g["passed"] is False]
            print(f"| {r['scenario']} #{r['rep']} | {r['score']:.2f} | {', '.join(r['skills_called']) or '(none)'} | {'; '.join(fails) or 'none'} |")
    print()
    print(f"Runs: {len(runs)}. Total agent cost: ${sum(r['cost_usd'] for r in runs):.2f} (judge calls not included).")


if __name__ == "__main__":
    main()
