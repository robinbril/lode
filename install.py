#!/usr/bin/env python3
"""Link the skills of this repository into the skill folders of Claude Code, Codex and Cursor.

Usage:
  python3 install.py          link what is missing
  python3 install.py --check  only report; exit 1 when lode, airesearch or council is missing

A skill that already exists somewhere else stays as it is and is reported.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SKILLS = {
    "lode": ROOT / "skills/lode",
    "airesearch": ROOT / "ai-architecture/skills/airesearch",
    "council": ROOT / "ai-architecture/skills/council",
    "ui-ophalen": ROOT / "frontend/skills/ui-ophalen",
    "rea": ROOT / "frontend/skills/rea",
    "pick-ui-library": ROOT / "frontend/skills/pick-ui-library",
}
REQUIRED = ("lode", "airesearch", "council")
CLIENTS = {"Claude Code": (".claude", "skills"), "Codex en andere": (".agents", "skills"), "Cursor": (".cursor", "skills")}


def state(link, source):
    if link.is_symlink() and link.resolve() == source:
        return "gelinkt"
    if link.exists():
        return "bestaat al, blijft staan"
    return "ontbreekt"


def main():
    only_check, missing = "--check" in sys.argv[1:], 0
    home = pathlib.Path.home()
    for client, (folder, skills) in CLIENTS.items():
        if folder != ".agents" and not (home / folder).is_dir():
            print(f"{client}: niet aanwezig")
            continue
        for name, source in SKILLS.items():
            link = home / folder / skills / name
            if link.is_symlink() and not link.exists() and not only_check:
                link.unlink()
            status = state(link, source)
            if status == "ontbreekt" and not only_check:
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(source)
                status = "gelinkt"
            missing += status == "ontbreekt" and name in REQUIRED
            print(f"{client}: {name} {status}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
