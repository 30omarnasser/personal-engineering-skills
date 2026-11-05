#!/usr/bin/env python3
"""Activation (triggering) test for the library's skills, driven by `claude -p`.

  python tools/activation_eval.py tests/activation_cases.json out.json [--workers 4] [--model M]

Builds a scratch project under the system temp dir with every installed-by-default skill copied
into <project>/.claude/skills, runs each prompt with `claude -p --max-turns 1`, and records which
Skill tool calls the model made (first turn by default; see --max-turns). A case passes when:
  * `expect` is a skill name and the model called it (a plugin-namespaced call such as
    `anthropic-skills:skill-creator` counts as `skill-creator`);
  * `expect` is null and the model called no library skill (optionally `expect_not` names one
    skill that must not be called);
  * cases without `expect` are observations and are reported but not scored.

Costs real tokens (about $0.35 per prompt on the default model in Nov 2026). Needs the `claude`
CLI logged in. Runs from inside a Claude Code session are fine: the CLAUDECODE guard is removed
for the subprocess. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fsutil import rmtree  # noqa: E402  (removes read-only .git files on Windows)

LIB = Path(__file__).resolve().parent.parent
CATS = ["01-core-engineering", "02-planning-architecture", "03-review-workflow",
        "04-security-correctness", "05-ai-engineering", "06-custom-domain"]


def run_error(result_ev: dict | None, usage: dict) -> str | None:
    """Why a run did not produce a real model turn, or None if it did."""
    if result_ev is None:
        return "no result event (CLI crashed, timed out or printed no stream-json)"
    if not usage.get("models"):
        return f"no model usage recorded: {(result_ev.get('result') or '')[:120]}"
    # error_max_turns is the normal end of a --max-turns 1 run whose first turn called a tool.
    if result_ev.get("is_error") and result_ev.get("subtype") != "error_max_turns":
        return f"result is_error ({result_ev.get('subtype')}): {(result_ev.get('result') or '')[:120]}"
    return None


def same_skill(called: str, expected: str) -> bool:
    """`anthropic-skills:skill-creator` satisfies an expectation of `skill-creator`."""
    return called == expected or called.endswith(":" + expected)


def build_project(root: Path) -> Path:
    proj = root / "skills-activation-project"
    if proj.exists():
        rmtree(proj)
    skills = proj / ".claude" / "skills"
    skills.mkdir(parents=True)
    for cat in CATS:
        if not (LIB / cat).is_dir():
            continue
        for d in sorted((LIB / cat).iterdir()):
            if (d / "SKILL.md").is_file():
                shutil.copytree(d, skills / d.name, ignore=shutil.ignore_patterns("__pycache__"))
    # A small realistic fixture: prompts name these files, and a project without them makes the
    # model spend its first turn searching instead of choosing a skill (measured: TDD 0/3 -> 2/2).
    fixture = {
        "README.md": "# Demo project\nFastAPI + RAG quotes service. Python 3.12, uv, pytest.\n",
        "pyproject.toml": '[project]\nname = "demo"\nversion = "0.1.0"\nrequires-python = ">=3.12"\n'
                          'dependencies = ["fastapi", "httpx"]\n\n[dependency-groups]\ndev = ["pytest"]\n',
        "app/__init__.py": "",
        "app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n",
        "app/pricing.py": "def line_total(qty, price):\n    return qty * price\n",
        "app/quotes.py": "def _merge_customer(q, c):\n    return {**q, 'customer': c['customer_id']}\n\n\n"
                         "def build_quote(q, c):\n    return _merge_customer(q, c)\n",
        "app/parsers.py": "def parse_rfq_reference(s):\n    raise NotImplementedError\n\n\n"
                          "def format_rfq_reference(r):\n    raise NotImplementedError\n",
        "app/routes/__init__.py": "",
        "app/routes/items.py": "def items(db, page: int = 1, size: int = 20):\n    return db[page*size:(page+1)*size]\n",
        "tests/__init__.py": "",
        "tests/test_quotes.py": "from app.quotes import build_quote\n\n\ndef test_build():\n"
                                "    assert build_quote({}, {'customer_id': 1})['customer'] == 1\n",
        "docs/SPEC.md": "# Quotes API spec\n\n1. Quotes MUST be scoped to the caller's tenant.\n"
                        "2. Totals MUST never be negative.\n",
        "docs/plan.md": "# Plan: quote PDF export\n\n- Route GET /quotes/{id}/pdf\n- A4, RTL support\n",
    }
    for rel_path, body in fixture.items():
        target = proj / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    if shutil.which("git"):
        subprocess.run(["git", "init", "-q"], cwd=proj, check=False)
        subprocess.run(["git", "add", "-A"], cwd=proj, check=False)
        subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"], cwd=proj,
                       check=False, capture_output=True)
    return proj


def run_case(case: dict, project: Path, model: str | None, timeout: int, claude: str, env: dict,
             max_turns: int = 1) -> dict:
    # The prompt goes over stdin, never argv: on Windows `claude` is an npm .cmd shim run by
    # cmd.exe, which cuts arguments at the first newline and silently drops every later flag.
    cmd = [claude, "-p", "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns)]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=project, env=env, input=case["prompt"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        out = p.stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
    skills, tools, text, usage, result_ev = [], [], "", {}, None
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools.append(c.get("name"))
                    if c.get("name") == "Skill":
                        skills.append(c.get("input", {}).get("skill", ""))
                elif c.get("type") == "text":
                    text += c.get("text", "")
        elif ev.get("type") == "result":
            result_ev = ev
            usage = {"cost_usd": ev.get("total_cost_usd"), "models": list((ev.get("modelUsage") or {}).keys())}
            text = text or (ev.get("result") or "")
    r = {**case, "skills_called": skills, "tools": tools, "text_head": text[:300], "usage": usage,
         "secs": round(time.time() - t0, 1)}
    # A run that never reached the model is an error, never a pass. Measured 2026-11-04: an account
    # usage limit returned "You've hit your 5-hour limit" with no model usage, and 24 negative cases
    # (expect: no skill) were counted as passes until this check existed.
    r["error"] = run_error(result_ev, usage)
    if r["error"]:
        r["pass"] = None
        return r
    if "expect" in case:
        exp = case["expect"]
        ok = any(same_skill(s, exp) for s in skills) if exp else (not skills)
        if case.get("expect_not"):
            ok = ok and not any(same_skill(s, case["expect_not"]) for s in skills)
        r["pass"] = ok
    else:
        r["pass"] = None
    return r


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cases")
    ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--model")
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--project", help="use this project instead of building a scratch one")
    ap.add_argument("--repeat", type=int, default=1, help="run every case N times (trigger-rate estimate)")
    ap.add_argument("--max-turns", type=int, default=1,
                    help="turns per prompt; >1 catches skills invoked after a first exploratory read "
                         "(tools then run in the scratch project, so keep it disposable)")
    a = ap.parse_args()
    claude = shutil.which("claude")
    if not claude:
        sys.exit("claude CLI not found on PATH")
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    project = Path(a.project) if a.project else build_project(Path(tempfile.gettempdir()))
    cases = json.loads(Path(a.cases).read_text(encoding="utf-8"))
    runs = [dict(c, id=f"{c['id']}#{k + 1}" if a.repeat > 1 else c["id"]) for c in cases for k in range(a.repeat)]
    results = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(run_case, c, project, a.model, a.timeout, claude, env, a.max_turns) for c in runs]
        for f in as_completed(futs):
            r = f.result()
            results.append(r)
            tag = "ERR " if r["error"] else {True: "PASS", False: "FAIL", None: "----"}[r["pass"]]
            print(f"[{tag}] {r['id']:30s} got={r['skills_called']} tools={r['tools'][:3]} {r['secs']}s"
                  + (f"  {r['error']}" if r["error"] else ""), flush=True)
    results.sort(key=lambda r: r["id"])
    Path(a.out).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n")
    errors = [r for r in results if r["error"]]
    scored = [r for r in results if r["pass"] is not None]
    passed = sum(1 for r in scored if r["pass"])
    cost = sum((r["usage"].get("cost_usd") or 0) for r in results)
    print(f"\n{passed}/{len(scored)} scored cases passed; {len(results) - len(scored) - len(errors)} observations; "
          f"{len(errors)} errored (not scored); cost ${cost:.2f}")
    print(f"project: {project}")
    if errors:
        print("ERRORS: re-run these cases; an errored run says nothing about the skill.")
        return 2
    return 0 if passed == len(scored) else 1


if __name__ == "__main__":
    sys.exit(main())
