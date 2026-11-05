#!/usr/bin/env python3
"""Check upstream repos for changes to the skills in this library.

  python tools/update.py            # clone upstream (shallow), diff every upstream skill, report
  python tools/update.py --apply    # also overwrite local copies with upstream and bump manifest commits

Needs git and network. Custom skills (06-custom-domain) are never touched.
Review the diff before --apply: upstream maintainers change instructions, and a
changed SKILL.md can change what your agent does.
"""
import argparse, difflib, filecmp, re, shutil, subprocess, sys, tempfile
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent
MANIFEST = LIB / "manifest.yaml"

# skill name -> (github repo, path inside repo)
UPSTREAM = {
    "systematic-debugging": ("obra/superpowers", "skills/systematic-debugging"),
    "verification-before-completion": ("obra/superpowers", "skills/verification-before-completion"),
    "test-driven-development": ("obra/superpowers", "skills/test-driven-development"),
    "requesting-code-review": ("obra/superpowers", "skills/requesting-code-review"),
    "using-git-worktrees": ("obra/superpowers", "skills/using-git-worktrees"),
    "handoff": ("mattpocock/skills", "skills/productivity/handoff"),
    "research": ("mattpocock/skills", "skills/engineering/research"),
    "grill-with-docs": ("mattpocock/skills", "skills/engineering/grill-with-docs"),
    "grilling": ("mattpocock/skills", "skills/productivity/grilling"),
    "domain-modeling": ("mattpocock/skills", "skills/engineering/domain-modeling"),
    "ask-matt": ("mattpocock/skills", "skills/engineering/ask-matt"),
    "spec-to-code-compliance": ("trailofbits/skills", "plugins/spec-to-code-compliance/skills/spec-to-code-compliance"),
    "property-based-testing": ("trailofbits/skills", "plugins/property-based-testing/skills/property-based-testing"),
    "supply-chain-risk-auditor": ("trailofbits/skills", "plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor"),
    "modern-python": ("trailofbits/skills", "plugins/modern-python/skills/modern-python"),
    "security-model": ("getsentry/skills", "skills/security-model"),
    "find-bugs": ("getsentry/skills", "skills/find-bugs"),
    "huggingface-local-models": ("huggingface/skills", "skills/huggingface-local-models"),
    "huggingface-best": ("huggingface/skills", "skills/huggingface-best"),
    "huggingface-community-evals": ("huggingface/skills", "skills/huggingface-community-evals"),
    "skill-creator": ("anthropics/skills", "skills/skill-creator"),
}


# Skills carrying local patches on top of upstream (see manifest.yaml `local_patches`).
# --apply overwrites them; re-apply the patches afterwards or keep the local copy.
LOCAL_PATCHES = {
    "handoff", "systematic-debugging", "test-driven-development", "verification-before-completion",
    "using-git-worktrees", "spec-to-code-compliance", "ask-matt",
    "find-bugs", "supply-chain-risk-auditor", "security-model", "skill-creator",
}


def read_utf8(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def local_path(name):
    for d in LIB.iterdir():
        if d.is_dir() and (d.name[:2].isdigit() or d.name == "_optional") and (d / name / "SKILL.md").is_file():
            return d / name
    return None


def diff_dirs(a: Path, b: Path):
    """Return list of (relpath, status) where status in added/removed/changed."""
    out = []
    fa = {p.relative_to(a) for p in a.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    fb = {p.relative_to(b) for p in b.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    for r in sorted(fb - fa): out.append((r, "added upstream"))
    for r in sorted(fa - fb): out.append((r, "removed upstream"))
    for r in sorted(fa & fb):
        if not filecmp.cmp(a / r, b / r, shallow=False): out.append((r, "changed"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--show", action="store_true", help="print unified diff of SKILL.md changes")
    a = ap.parse_args()
    if sys.platform == "win32":  # keep non-cp1252 characters in diffs from crashing the run
        for stream in (sys.stdout, sys.stderr):
            stream.reconfigure(encoding="utf-8", errors="replace")
    tmp = Path(tempfile.mkdtemp(prefix="skills-upstream-"))
    try:
        run(a, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # shallow clones are ~100 MB; never leave them behind


def run(a, tmp: Path):
    repos = {}
    for repo, _ in UPSTREAM.values():
        if repo in repos: continue
        dest = tmp / repo.replace("/", "_")
        print(f"cloning {repo} ...", flush=True)
        # autocrlf=false: with Git for Windows defaults the clone gets CRLF endings and every
        # file reads as "changed" even when upstream is byte-identical.
        subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--depth", "1",
                        f"https://github.com/{repo}", str(dest)], check=True)
        sha = subprocess.run(["git", "-C", str(dest), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        repos[repo] = (dest, sha)
    manifest = read_utf8(MANIFEST) if MANIFEST.exists() else ""
    changed_any = False
    for name, (repo, sub) in UPSTREAM.items():
        loc = local_path(name)
        if loc is None: continue
        up = repos[repo][0] / sub
        if not up.is_dir():
            print(f"!! {name}: upstream path moved or removed ({repo}/{sub}) — check the repo"); continue
        d = diff_dirs(loc, up)
        if not d:
            print(f"   {name}: up to date"); continue
        changed_any = True
        patched = "  [has local patches — see manifest local_patches]" if name in LOCAL_PATCHES else ""
        print(f"** {name} ({repo} @ {repos[repo][1]}):{patched}")
        for r, st in d: print(f"     {st:16s} {r}")
        if a.show and (loc / "SKILL.md").exists() and (up / "SKILL.md").exists():
            sys.stdout.writelines(difflib.unified_diff(
                read_utf8(loc / "SKILL.md").splitlines(True), read_utf8(up / "SKILL.md").splitlines(True),
                f"local/{name}/SKILL.md", f"upstream/{name}/SKILL.md"))
        if a.apply:
            shutil.rmtree(loc); shutil.copytree(up, loc, ignore=shutil.ignore_patterns("__pycache__"))
            manifest = re.sub(rf"(  - name: {re.escape(name)}\n(?:    .*\n)*?    commit: )\S+", rf"\g<1>{repos[repo][1]}", manifest)
            manifest = re.sub(rf"(  - name: {re.escape(name)}\n(?:    .*\n)*?    last_evaluated: )\S+", r"\g<1>null  # re-test after update", manifest)
            print(f"     -> applied" + ("  !! local patches lost; re-apply them" if name in LOCAL_PATCHES else ""))
    if a.apply and changed_any:
        MANIFEST.write_text(manifest, encoding="utf-8"); print("manifest.yaml updated")
    if not changed_any: print("\nAll upstream skills unchanged.")
    elif not a.apply: print("\nRe-run with --apply to overwrite local copies (and --show to see SKILL.md diffs first).")


if __name__ == "__main__":
    main()
