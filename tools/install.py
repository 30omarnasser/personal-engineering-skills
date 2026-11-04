#!/usr/bin/env python3
"""Install skills from this library into Claude Code (global) or a project.

Usage (run from anywhere; the library location is found from this file):
  python tools/install.py global                 # 01, 02, 03, 07 -> ~/.claude/skills
  python tools/install.py project /path/to/repo  # interactive pick from 04, 05, 06 -> <repo>/.claude/skills
  python tools/install.py project . --all        # all project-scope skills, no prompt
  python tools/install.py project . --pick security-model,rag-evaluation
  python tools/install.py hook                   # PreCompact transcript backup hook
  python tools/install.py list                   # show what would go where

Skills are COPIED (not symlinked) so a project works when cloned elsewhere.
Re-running overwrites the skill folders it installs; it never deletes other skills.
Other agents (Codex, Cursor, etc.): pass --dest <their skills dir>.
"""
import argparse, json, shutil, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent
GLOBAL_CATS = ["01-core-engineering", "02-planning-architecture", "03-review-workflow", "07-skill-development"]
PROJECT_CATS = ["04-security-correctness", "05-ai-engineering", "06-custom-domain"]


def skills_in(cats):
    out = []
    for c in cats:
        d = LIB / c
        if d.is_dir():
            out += sorted(p for p in d.iterdir() if (p / "SKILL.md").is_file())
    return out


def copy_skill(src: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / src.name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store", "*-workspace"))
    print(f"  + {src.parent.name}/{src.name}  ->  {target}")


def cmd_global(a):
    dest = Path(a.dest).expanduser() if a.dest else Path.home() / ".claude" / "skills"
    print(f"Installing global skills to {dest}")
    for s in skills_in(GLOBAL_CATS):
        copy_skill(s, dest)


def cmd_project(a):
    repo = Path(a.repo).expanduser().resolve()
    if not repo.is_dir():
        sys.exit(f"not a directory: {repo}")
    dest = Path(a.dest).expanduser() if a.dest else repo / ".claude" / "skills"
    avail = skills_in(PROJECT_CATS)
    if a.all:
        chosen = avail
    elif a.pick:
        names = {n.strip() for n in a.pick.split(",")}
        chosen = [s for s in avail if s.name in names]
        missing = names - {s.name for s in chosen}
        if missing:
            sys.exit(f"unknown skills: {', '.join(sorted(missing))}")
    else:
        print("Project-scope skills available:")
        for i, s in enumerate(avail, 1):
            print(f"  {i:2d}. {s.parent.name}/{s.name}")
        raw = input("Numbers to install (comma-separated, or 'all'): ").strip()
        chosen = avail if raw == "all" else [avail[int(x) - 1] for x in raw.split(",") if x.strip()]
    print(f"Installing {len(chosen)} skill(s) to {dest}")
    for s in chosen:
        copy_skill(s, dest)
    tmpl = LIB / "templates" / "AGENTS.md"
    for name in ("AGENTS.md", "CLAUDE.md"):
        if (repo / name).exists():
            break
    else:
        if tmpl.exists():
            shutil.copy2(tmpl, repo / "AGENTS.md")
            print(f"  + AGENTS.md template -> {repo / 'AGENTS.md'}  (edit the TODOs)")


def cmd_hook(a):
    home = Path.home() / ".claude"
    hooks = home / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    src = LIB / "_infra" / "precompact-backup" / "precompact_backup.py"
    shutil.copy2(src, hooks / src.name)
    settings = home / "settings.json"
    cfg = json.loads(settings.read_text()) if settings.exists() else {}
    cmd = f"python3 {hooks / src.name}" if sys.platform != "win32" else f'python "{hooks / src.name}"'
    entry = {"matcher": "", "hooks": [{"type": "command", "command": cmd}]}
    pre = cfg.setdefault("hooks", {}).setdefault("PreCompact", [])
    if not any("precompact_backup" in h.get("command", "") for e in pre for h in e.get("hooks", [])):
        pre.append(entry)
        settings.write_text(json.dumps(cfg, indent=2))
        print(f"  + PreCompact hook added to {settings}")
    else:
        print("  = PreCompact hook already configured")


def cmd_list(a):
    for label, cats in (("GLOBAL  (~/.claude/skills)", GLOBAL_CATS), ("PROJECT (<repo>/.claude/skills)", PROJECT_CATS)):
        print(label)
        for s in skills_in(cats):
            print(f"  {s.parent.name}/{s.name}")


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
g = sub.add_parser("global"); g.add_argument("--dest"); g.set_defaults(f=cmd_global)
pr = sub.add_parser("project"); pr.add_argument("repo"); pr.add_argument("--all", action="store_true")
pr.add_argument("--pick"); pr.add_argument("--dest"); pr.set_defaults(f=cmd_project)
sub.add_parser("hook").set_defaults(f=cmd_hook)
sub.add_parser("list").set_defaults(f=cmd_list)
args = p.parse_args()
args.f(args)
