#!/usr/bin/env python3
"""Check every source line in every card against the pinned commit on GitHub.

Usage: python3 check.py [card.md ...]

A source line is `- owner/repo@sha path:line "keyword"` or `- https://url (gelezen date) "keyword"`.
The keyword must be on the line or within two lines of it. Files come from
raw.githubusercontent.com and stay in .cache/. Web sources are counted, not fetched.
"""
import concurrent.futures
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
AREAS = ("ai-architecture", "backend", "frontend")
FIELDS = ("Probleem:", "Oplossing:", "Waarom het werkt:", "Niet doen als:", "Toetsvraag:", "Bronnen:")
CODE = re.compile(r'- ([\w.-]+/[\w.-]+)@([0-9a-f]{7,40}) (.+?):(\d+)(?:-\d+)? "(.+)"')
WEB = re.compile(r'- https://\S+ \(gelezen \d{4}-\d\d-\d\d\) ".+"')
MAX_LINES = 60


def fetch(repo, sha, path):
    cached = ROOT / ".cache" / repo / sha / path
    if cached.is_file():
        return cached.read_text(encoding="utf-8", errors="replace")
    url = f"https://raw.githubusercontent.com/{repo}/{sha}/{urllib.parse.quote(path)}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data.decode("utf-8", errors="replace")


def check_code(match):
    repo, sha, path, line, keyword = match.groups()
    try:
        lines = fetch(repo, sha, path).splitlines()
    except (urllib.error.URLError, OSError) as error:
        return f"niet op te halen: {error}"
    number = int(line)
    if not 1 <= number <= len(lines):
        return f"bestand heeft {len(lines)} regels"
    if keyword not in "\n".join(lines[max(0, number - 3):number + 2]):
        return "kernwoord staat er niet"
    return None


def read_card(card):
    text = card.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors = [f"mist {field}" for field in FIELDS if field not in text]
    if len(lines) > MAX_LINES:
        errors.append(f"{len(lines)} regels")
    after = text.split("Bronnen:", 1)[-1].splitlines()
    sources = [line.strip() for line in after if line.strip().startswith("- ")]
    code = [(line, CODE.fullmatch(line)) for line in sources]
    web = [line for line, match in code if match is None and WEB.fullmatch(line)]
    errors += [f"onleesbare bron {line}" for line, match in code if match is None and line not in web]
    if not sources:
        errors.append("geen bron")
    return errors, [(line, match) for line, match in code if match], web


def check_index(cards):
    """AGENTS.md names every card once or more, and no card that does not exist."""
    path, area, named = ROOT / "AGENTS.md", None, set()
    if not path.is_file():
        return ["AGENTS.md ontbreekt"]
    for line in path.read_text(encoding="utf-8").splitlines():
        if match := re.search(r"Kaarten in `([\w-]+)/kaarten/`", line):
            area = match.group(1)
        elif line.startswith("## "):
            area = None
        elif area and line.startswith("| "):
            named |= {(area, number) for number in re.findall(r"\b\d\d\b", line.split("|")[2])}
    present = {(card.parent.parent.name, card.name[:2]) for card in cards}
    return [f"AGENTS.md mist {a}/{n}" for a, n in sorted(present - named)] + [
        f"AGENTS.md noemt {a}/{n}, die bestaat niet" for a, n in sorted(named - present)]


def known_repos():
    path = ROOT / "sources.json"
    return {s.get("repo") for s in json.loads(path.read_text())} if path.is_file() else None


def main():
    cards = [pathlib.Path(a).resolve() for a in sys.argv[1:]] or sorted(
        card for area in AREAS for card in (ROOT / area / "kaarten").glob("[0-9][0-9]-*.md") if card.name != "00-keuze.md")
    failures, jobs, web_total, repos = [], [], 0, known_repos()
    if not sys.argv[1:]:
        failures += check_index(cards)
    for card in cards:
        errors, code, web = read_card(card)
        failures += [f"{card.relative_to(ROOT)}: {error}" for error in errors]
        web_total += len(web)
        jobs += [(card, line, match) for line, match in code]
    with concurrent.futures.ThreadPoolExecutor(12) as pool:
        results = list(pool.map(lambda job: check_code(job[2]), jobs))
    for (card, line, match), error in zip(jobs, results):
        if error:
            failures.append(f"{card.relative_to(ROOT)}: {error}: {line}")
        if repos is not None and match.group(1) not in repos:
            failures.append(f"{card.relative_to(ROOT)}: {match.group(1)} staat niet in sources.json")
    good = sum(1 for error in results if error is None)
    print(*failures, sep="\n")
    print(f"{len(cards)} kaarten, {good} van {len(jobs)} codebronnen goed, {web_total} webbronnen niet gecontroleerd, {len(failures)} fouten")
    sys.exit(1 if failures or not cards else 0)


if __name__ == "__main__":
    main()
