#!/usr/bin/env python3
"""Static checks for this skill library. Run before committing and after tools/update.py.

  python tools/check_library.py            # structure, frontmatter, links, manifest, encoding
  python tools/check_library.py --scripts  # also run the vendored script test suites (needs pytest)

Exit 0 when everything passes, 1 otherwise. Stdlib only.

Checks:
  * every skill directory has a SKILL.md with YAML-ish frontmatter: name == directory name,
    description present, <= 1024 chars (agent-skills spec) and no angle brackets
  * frontmatter keys are ones Claude Code or the agent-skills spec understand
  * manual-only skills declare `disable-model-invocation: true` and the manifest agrees
  * manifest.yaml lists every skill exactly once, with the category it actually lives in
  * tools/update.py knows the upstream path of every non-custom skill
  * every relative markdown link resolves (example paths under GLOSSARY-FORMAT are exempt)
  * files are UTF-8 with LF line endings and carry no bidi/zero-width characters
    (the fenced-example trick in spec-to-code-compliance's ANALYSIS_FORMAT.md is exempt)
  * no plugin-namespaced skill references (`superpowers:` etc.) that cannot resolve here
  * every .py compiles; every .sh passes `bash -n` when bash is available
"""
from __future__ import annotations

import argparse
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent
SKILL_DIRS = [p for p in LIB.iterdir() if p.is_dir() and (p.name[:2].isdigit() or p.name == "_optional")]

# Claude Code skill frontmatter (code.claude.com/docs/en/skills) plus the agent-skills spec keys.
ALLOWED_KEYS = {
    "name", "description", "license", "allowed-tools", "disallowed-tools", "metadata", "compatibility",
    "argument-hint", "arguments", "disable-model-invocation", "user-invocable", "effort", "model",
    "context", "agent", "background", "shell", "hooks", "paths", "when_to_use",
}
MANUAL_SKILLS = {"handoff", "grill-with-docs", "ask-matt"}
CUSTOM_SKILLS = {"context-continuity-check", "procurement-evidence-review", "rag-evaluation"}
HIDDEN_EXEMPT = {"04-security-correctness/spec-to-code-compliance/resources/ANALYSIS_FORMAT.md"}
LINK_EXEMPT_FILES = {"02-planning-architecture/domain-modeling/GLOSSARY-FORMAT.md"}
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".toml", ".txt", ".html", ".ts", ".example"}

problems: list[str] = []


def fail(msg: str) -> None:
    problems.append(msg)


def rel(p: Path) -> str:
    return p.relative_to(LIB).as_posix()


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not m:
        return None
    out: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t")) and key:
            out[key] += " " + line.strip()
            continue
        if ":" in line and not line.startswith(("#", "-")):
            key, _, val = line.partition(":")
            out[key.strip()] = val.strip()
    for k, v in out.items():
        if v[:1] in {">", "|"}:
            v = v[1:].lstrip("-+ ")
        out[k] = v.strip().strip('"').strip("'")
    return out


def skills() -> list[Path]:
    out = []
    for cat in SKILL_DIRS:
        for d in sorted(cat.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                out.append(d)
    return out


def check_skill(d: Path) -> dict[str, str]:
    md = d / "SKILL.md"
    if not md.is_file():
        fail(f"{rel(d)}: no SKILL.md")
        return {}
    fm = parse_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
    if fm is None:
        fail(f"{rel(md)}: no frontmatter")
        return {}
    unknown = set(fm) - ALLOWED_KEYS
    if unknown:
        fail(f"{rel(md)}: unknown frontmatter keys {sorted(unknown)}")
    if fm.get("name") != d.name:
        fail(f"{rel(md)}: name '{fm.get('name')}' != directory '{d.name}'")
    desc = fm.get("description", "")
    if not desc:
        fail(f"{rel(md)}: empty description")
    if len(desc) > 1024:
        fail(f"{rel(md)}: description is {len(desc)} chars (> 1024)")
    if "<" in desc or ">" in desc:
        fail(f"{rel(md)}: description contains angle brackets")
    manual = fm.get("disable-model-invocation", "").lower() == "true"
    if (d.name in MANUAL_SKILLS) != manual:
        fail(f"{rel(md)}: disable-model-invocation={manual} but MANUAL_SKILLS says {d.name in MANUAL_SKILLS}")
    for item in ("allowed-tools",):
        if item in fm and not fm[item]:
            fail(f"{rel(md)}: empty {item}")
    return fm


def check_manifest(found: dict[str, Path]) -> None:
    mf = LIB / "manifest.yaml"
    if not mf.is_file():
        fail("manifest.yaml missing")
        return
    text = mf.read_text(encoding="utf-8")
    entries = re.findall(r"  - name: (\S+)\n(?:    .*\n?)*?    category: (\S+)", text)
    names = [n for n, _ in entries]
    for n in set(names):
        if names.count(n) > 1:
            fail(f"manifest.yaml: '{n}' listed {names.count(n)} times")
    for n, cat in entries:
        if n not in found:
            fail(f"manifest.yaml: '{n}' has no directory")
        elif found[n].parent.name != cat:
            fail(f"manifest.yaml: '{n}' category {cat} but lives in {found[n].parent.name}")
    for n in found:
        if n not in names:
            fail(f"manifest.yaml: '{n}' not listed")
    for n, cat in entries:
        block = re.search(rf"  - name: {re.escape(n)}\n((?:    .*\n?)*)", text).group(1)
        act = re.search(r"activation: (\S+)", block)
        want = "manual" if n in MANUAL_SKILLS else "auto"
        if not act or act.group(1) != want:
            fail(f"manifest.yaml: '{n}' activation should be {want}")


def check_update_tool(found: dict[str, Path]) -> None:
    src = (LIB / "tools" / "update.py").read_text(encoding="utf-8")
    known = set(re.findall(r'^\s+"([a-z0-9-]+)": \("', src, re.M))
    for n in found:
        if n not in CUSTOM_SKILLS and n not in known:
            fail(f"tools/update.py: no UPSTREAM entry for '{n}'")
    for n in known:
        if n not in found:
            fail(f"tools/update.py: UPSTREAM entry '{n}' has no directory")
    m = re.search(r"LOCAL_PATCHES = \{(.*?)\}", src, re.S)
    patched_tool = set(re.findall(r'"([a-z0-9-]+)"', m.group(1))) if m else set()
    manifest = (LIB / "manifest.yaml").read_text(encoding="utf-8")
    patched_manifest = {n for n, blk in re.findall(r"  - name: (\S+)\n((?:    .*\n?)*)", manifest)
                        if "local_patches:" in blk and n not in CUSTOM_SKILLS}
    if patched_tool != patched_manifest:
        fail(f"tools/update.py LOCAL_PATCHES and manifest local_patches disagree: "
             f"only in update.py {sorted(patched_tool - patched_manifest)}, "
             f"only in manifest {sorted(patched_manifest - patched_tool)}")


def check_text_files() -> None:
    link_re = re.compile(r"\]\(([^)\s]+)\)")
    for p in LIB.rglob("*"):
        if not p.is_file() or ".git" in p.parts or "__pycache__" in p.parts or "_licenses" in p.parts:
            continue
        if p.suffix not in TEXT_SUFFIXES and p.name != "LICENSE.txt":
            continue
        raw = p.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            fail(f"{rel(p)}: not UTF-8")
            continue
        if b"\r\n" in raw:
            fail(f"{rel(p)}: CRLF line endings")
        if rel(p) not in HIDDEN_EXEMPT:
            for i, ch in enumerate(text):
                if ch in "\n\r\t" or (i == 0 and ch == "\ufeff"):
                    continue
                if unicodedata.category(ch) in {"Cc", "Cf", "Zl", "Zp"}:
                    fail(f"{rel(p)}: hidden character U+{ord(ch):04X} {unicodedata.name(ch, '?')}")
                    break
        if p.suffix == ".md" and rel(p) not in LINK_EXEMPT_FILES:
            for m in link_re.finditer(text):
                link = m.group(1).split("#")[0].strip("<>")
                if not link or link.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (p.parent / link).exists():
                    fail(f"{rel(p)}: broken link '{link}'")
            for m in re.finditer(r"`(superpowers|anthropic-skills|trailofbits)[:/][a-z-]+`", text):
                if p.name == "SKILL.md":
                    fail(f"{rel(p)}: plugin-namespaced reference {m.group(0)} will not resolve here")
        if p.suffix == ".py":
            try:
                py_compile.compile(str(p), doraise=True, cfile=None)
            except py_compile.PyCompileError as e:
                fail(f"{rel(p)}: does not compile: {e.msg.splitlines()[0]}")
        if p.suffix == ".sh" and shutil.which("bash"):
            r = subprocess.run(["bash", "-n", str(p)], capture_output=True, text=True)
            if r.returncode:
                fail(f"{rel(p)}: bash -n failed: {r.stderr.strip()[:120]}")


def run_script_suites() -> None:
    suites = [
        (LIB / "04-security-correctness/security-model/scripts", ["selftest_resolve_security_model.py"]),
        (LIB / "04-security-correctness/supply-chain-risk-auditor/scripts",
         ["test_model.py", "test_render.py", "test_sources.py", "test_collect.py"]),
        (LIB / "tests", ["test_check_library.py", "test_e2e_fixtures.py", "test_harness_guards.py"]),
    ]
    # The resolver's "non-git walk" test builds a repo-less tree under the temp dir; if the
    # user's home itself is a git repository, git would otherwise discover it from there.
    env = dict(os.environ, GIT_CEILING_DIRECTORIES=tempfile.gettempdir())
    for cwd, files in suites:
        print(f"-- pytest in {rel(cwd)}")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *files],
                           cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print("   " + tail)
        if r.returncode:
            fail(f"{rel(cwd)}: test suite failed ({tail})")
    for pyc in LIB.rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scripts", action="store_true", help="also run the vendored pytest suites")
    a = ap.parse_args()
    found: dict[str, Path] = {}
    for d in skills():
        fm = check_skill(d)
        if fm.get("name"):
            found[fm["name"]] = d
    check_manifest(found)
    check_update_tool(found)
    check_text_files()
    if a.scripts:
        run_script_suites()
    for pyc in LIB.rglob("__pycache__"):
        shutil.rmtree(pyc, ignore_errors=True)
    print(f"{len(found)} skills checked")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print("  - " + p)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
