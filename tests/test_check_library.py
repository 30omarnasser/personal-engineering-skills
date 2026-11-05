"""Mutation tests for tools/check_library.py: each seeded defect must be reported.

Run: python -m pytest -q tests/test_check_library.py   (also run by check_library.py --scripts)
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

LIB = Path(__file__).resolve().parent.parent

# label: (file, old text or None for "convert to CRLF", new text, expected message fragment)
MUTATIONS = {
    "name-dir-mismatch": ("01-core-engineering/research/SKILL.md", "name: research", "name: researcher",
                          "name 'researcher' != directory"),
    "unknown-frontmatter-key": ("01-core-engineering/handoff/SKILL.md", "argument-hint:", "argument_hint:",
                                "unknown frontmatter keys"),
    "broken-link": ("04-security-correctness/property-based-testing/SKILL.md", "references/generating.md)",
                    "references/missing.md)", "broken link"),
    "plugin-namespaced-ref": ("01-core-engineering/systematic-debugging/SKILL.md",
                              "Use the `test-driven-development` skill",
                              "Use the `superpowers:test-driven-development` skill", "plugin-namespaced"),
    "manual-skill-auto-invocable": ("02-planning-architecture/ask-matt/SKILL.md", "disable-model-invocation: true\n",
                                    "", "disable-model-invocation=False"),
    "hidden-bidi-char": ("06-custom-domain/rag-evaluation/SKILL.md", "# RAG Evaluation", "# RAG \u202eEvaluation",
                         "hidden character U+202E"),
    "crlf": ("06-custom-domain/procurement-evidence-review/SKILL.md", None, None, "CRLF line endings"),
    "manifest-drift": ("manifest.yaml", "  - name: find-bugs\n", "  - name: find-bugz\n", "'find-bugz' has no directory"),
}


def run_check(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(root / "tools" / "check_library.py")],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


@pytest.fixture
def lib_copy(tmp_path: Path) -> Path:
    dst = tmp_path / "lib"
    shutil.copytree(LIB, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", "tests"))
    return dst


def test_clean_library_passes(lib_copy: Path) -> None:
    r = run_check(lib_copy)
    assert r.returncode == 0, r.stdout


@pytest.mark.parametrize("label", sorted(MUTATIONS))
def test_seeded_defect_is_reported(lib_copy: Path, label: str) -> None:
    rel, old, new, expect = MUTATIONS[label]
    f = lib_copy / rel
    if old is None:
        f.write_bytes(f.read_bytes().replace(b"\n", b"\r\n"))
    else:
        text = f.read_text(encoding="utf-8")
        assert old in text, f"fixture drifted: {old!r} not in {rel}"
        f.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    r = run_check(lib_copy)
    assert r.returncode == 1 and expect in r.stdout, r.stdout
