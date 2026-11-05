"""Guards that stop the eval harnesses from scoring runs that never reached the model.

Regression for 2026-11-04: an account usage limit returned "You've hit your 5-hour limit" with no
model usage, and the activation harness counted 24 "no skill should fire" cases as passes.
No model calls: `claude` is replaced with a fake that prints canned stream-json.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

LIB = Path(__file__).resolve().parent.parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, LIB / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


act = load("activation_eval")

LIMIT = {"type": "result", "subtype": "success", "is_error": True, "result": "You've hit your 5-hour limit",
         "modelUsage": {}, "total_cost_usd": 0}
OK = {"type": "result", "subtype": "success", "is_error": False, "result": "done",
      "modelUsage": {"claude-opus-5-5": {}}, "total_cost_usd": 0.01}


def fake_claude(tmp_path: Path, events: list[dict]) -> str:
    """A stand-in CLI: a Python script that prints the given stream-json lines."""
    script = tmp_path / "fake_claude.py"
    script.write_text("import sys\nsys.stdin.read()\n" + "".join(f"print({json.dumps(json.dumps(e))})\n" for e in events),
                      encoding="utf-8")
    return str(script)


def run(tmp_path: Path, events: list[dict], case: dict, monkeypatch: pytest.MonkeyPatch) -> dict:
    script = fake_claude(tmp_path, events)
    real_run = act.subprocess.run

    def patched(cmd, **kw):
        return real_run([sys.executable, script, *cmd[1:]], **kw)

    monkeypatch.setattr(act.subprocess, "run", patched)
    return act.run_case(case, tmp_path, None, 30, "claude", {})


NEG = {"id": "neg", "prompt": "hi", "expect": None}
POS = {"id": "pos", "prompt": "hi", "expect": "rag-evaluation"}


def test_usage_limit_is_an_error_not_a_pass(tmp_path, monkeypatch):
    r = run(tmp_path, [LIMIT], NEG, monkeypatch)
    assert r["pass"] is None and "limit" in r["error"]


def test_missing_result_event_is_an_error(tmp_path, monkeypatch):
    r = run(tmp_path, [], NEG, monkeypatch)
    assert r["pass"] is None and "no result event" in r["error"]


def test_no_model_usage_is_an_error(tmp_path, monkeypatch):
    r = run(tmp_path, [dict(OK, modelUsage={})], NEG, monkeypatch)
    assert r["pass"] is None and "no model usage" in r["error"]


def test_max_turns_end_is_a_valid_run(tmp_path, monkeypatch):
    # --max-turns 1 ends with error_max_turns whenever turn 1 calls a tool; that run is real.
    tool = {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Glob", "input": {}}]}}
    r = run(tmp_path, [tool, dict(OK, is_error=True, subtype="error_max_turns", result="")], NEG, monkeypatch)
    assert r["error"] is None and r["pass"] is True


def test_other_error_subtypes_are_errors(tmp_path, monkeypatch):
    r = run(tmp_path, [dict(OK, is_error=True, subtype="error_during_execution")], NEG, monkeypatch)
    assert r["pass"] is None and "error_during_execution" in r["error"]


def test_real_negative_still_passes(tmp_path, monkeypatch):
    r = run(tmp_path, [OK], NEG, monkeypatch)
    assert r["error"] is None and r["pass"] is True


def test_real_positive_scores_skill_call(tmp_path, monkeypatch):
    call = {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill",
                                                          "input": {"skill": "rag-evaluation"}}]}}
    r = run(tmp_path, [call, OK], POS, monkeypatch)
    assert r["error"] is None and r["pass"] is True


def test_namespaced_skill_matches():
    assert act.same_skill("anthropic-skills:skill-creator", "skill-creator")
    assert not act.same_skill("requesting-code-review", "code-review")
