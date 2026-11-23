#!/usr/bin/env python3
"""Copy complete codebases into the three areas, byte for byte, and check them.

Usage:
  python3 copy.py take  [name ...]   stage the codebase in <area>/<map>/
  python3 copy.py check [name ...]   compare the committed copy with the maker's commit

codebases.json names url, commit, licence, area and folder per codebase. Every file that is copied has
the maker's exact bytes. `reason` says what stays out. Files that steer an agent or git get
`.bron` after their name, so that nobody's rules load by accident.
"""
import collections
import fnmatch
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / "codebases.json"
RENAME = {".claude", ".codex", ".cursor", ".agents", ".opencode", ".gemini", ".windsurf", ".mcp.json", "AGENTS.md",
          "CLAUDE.md", "GEMINI.md", "CLAUDE.local.md", ".cursorrules", ".gitattributes", ".gitmodules", ".gitignore"}
SKIP_DIRS = {".github", "ee", "enterprise", "node_modules", "cassettes", "__snapshots__", "snapshots"}
LOCAL = re.compile(r"(^|/)\.env(\.local|\.production)?$|\.DS_Store$")
MEDIA = re.compile(r"\.(png|jpe?g|gif|webp|avif|mp4|mov|webm|mp3|wav|pdf|zip|gz|tgz|ico|icns|psd)$", re.I)
MAX_BYTES, MAX_MEDIA = 1_000_000, 100_000
LOCKFILES = {"pnpm-lock.yaml", "package-lock.json", "yarn.lock", "bun.lock", "uv.lock", "Cargo.lock", "poetry.lock", "go.sum"}
Entry = collections.namedtuple("Entry", "mode sha size path")


def git(*args, stdin=None):
    return subprocess.run(["git", "-C", str(ROOT), *args], input=stdin, capture_output=True, check=True).stdout


def target(path):
    return "/".join(part + ".bron" if part in RENAME else part for part in path.split("/"))


def reason(entry, spec):
    """Why a file of the maker stays out, or None."""
    parts = entry.path.split("/")
    if entry.mode == "160000":
        return "submodule"
    if entry.mode == "120000":
        return "link"
    if SKIP_DIRS.intersection(parts[:-1]):
        return "map"
    if LOCAL.search(entry.path):
        return "lokaal bestand"
    if any(fnmatch.fnmatch(entry.path, pattern) for pattern in spec.get("without", [])):
        return "uitgesloten"
    if parts[-1] not in LOCKFILES and entry.size > (MAX_MEDIA if MEDIA.search(entry.path) else MAX_BYTES):
        return "te groot"
    return None


def fetch(spec):
    has = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", spec["commit"] + "^{tree}"], capture_output=True)
    if has.returncode == 0:
        return
    for attempt in range(3):
        done = subprocess.run(["git", "-C", str(ROOT), "fetch", "-q", "--depth", "1", "--no-tags", "--no-auto-gc",
                               spec["url"], spec["commit"]], capture_output=True)
        if done.returncode == 0:
            return
    sys.exit(f"{spec['url']}: {done.stderr.decode()}")


def wanted(spec):
    """The entries that belong in the copy, and how many stay out per reason."""
    fetch(spec)
    out = git("ls-tree", "-r", "-l", "-z", spec["commit"]).decode("utf-8", "surrogateescape")
    keep, left = [], collections.Counter()
    for record in filter(None, out.split("\0")):
        meta, path = record.split("\t", 1)
        mode, _, sha, size = meta.split()
        entry = Entry(mode, sha, 0 if size == "-" else int(size), path)
        why = reason(entry, spec)
        if why:
            left[why] += 1
        else:
            keep.append(entry)
    return keep, left


def take(name, spec):
    keep, left = wanted(spec)
    folder = f"{spec['area']}/{spec['map']}"
    git("rm", "-r", "-q", "--cached", "--ignore-unmatch", folder)
    lines = "".join(f"{e.mode} {e.sha}\t{folder}/{target(e.path)}\0" for e in keep)
    git("update-index", "-z", "--index-info", stdin=lines.encode("utf-8", "surrogateescape"))
    git("checkout-index", "-f", "-z", "--stdin",
        stdin="".join(f"{folder}/{target(e.path)}\0" for e in keep).encode("utf-8", "surrogateescape"))
    spec["files"] = len(keep)
    return f"{name}: {len(keep)} bestanden, {sum(e.size for e in keep) / 1e6:.1f} MB, weg {dict(left)}"


def check(name, spec):
    keep, _ = wanted(spec)
    want = {target(e.path): (e.mode, e.sha) for e in keep}
    folder = f"{spec['area']}/{spec['map']}/"
    out = git("ls-tree", "-r", "-z", "HEAD", folder).decode("utf-8", "surrogateescape")
    have = {}
    for record in filter(None, out.split("\0")):
        meta, path = record.split("\t", 1)
        mode, _, sha = meta.split()
        have[path[len(folder):]] = (mode, sha)
    wrong = sorted(p for p in want.keys() | have.keys() if want.get(p) != have.get(p))
    if wrong:
        return f"{name}: {len(wrong)} verschillen, eerste {wrong[0]}", len(wrong)
    return f"{name}: {len(have)} bestanden gelijk aan de maker", 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("take", "check"):
        sys.exit(__doc__)
    manifest, failures = json.loads(MANIFEST.read_text(encoding="utf-8")), 0
    for name in sys.argv[2:] or sorted(manifest):
        if sys.argv[1] == "take":
            print(take(name, manifest[name]), flush=True)
            MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            line, wrong = check(name, manifest[name])
            failures += wrong
            print(line, flush=True)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
