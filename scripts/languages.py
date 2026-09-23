#!/usr/bin/env python3
"""Draw metrics/languages.svg from the lines I wrote, read from local clones.

Runs on this machine only. Nothing but language totals leaves it: no repo names,
paths or code end up in the SVG, so private repos can be counted
without being uploaded anywhere.

    python3 scripts/languages.py            # scan ~/developer, write the SVG
    python3 scripts/languages.py --dry-run  # print the table, write nothing
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOTS = [Path.home() / "developer"]
# Author emails and skipped directory names live in a gitignored file so they
# never reach this public repo. One entry per line: an email, or "skip <name>".
LOCAL_CONFIG = Path(__file__).resolve().parent / "authors.local"

LANGUAGES = {
    ".cs": "C#", ".csx": "C#",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".mts": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".py": "Python", ".sql": "SQL", ".php": "PHP", ".lua": "Lua",
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell", ".ps1": "PowerShell",
    ".css": "CSS", ".scss": "SCSS", ".html": "HTML", ".cshtml": "Razor", ".razor": "Razor",
    ".hbs": "Handlebars", ".ejs": "EJS", ".go": "Go", ".rs": "Rust", ".java": "Java",
    ".kt": "Kotlin", ".dart": "Dart", ".vue": "Vue", ".svelte": "Svelte",
}
COLOURS = {  # GitHub linguist colours
    "C#": "#178600", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5",
    "SQL": "#e38c00", "PHP": "#4F5D95", "Lua": "#000080", "Shell": "#89e051",
    "PowerShell": "#012456", "CSS": "#663399", "SCSS": "#c6538c", "HTML": "#e34c26",
    "Razor": "#512be4", "Handlebars": "#f7931e", "EJS": "#a91e50", "Go": "#00ADD8",
    "Rust": "#dea584", "Java": "#b07219", "Kotlin": "#A97BFF", "Dart": "#00B4AB",
    "Vue": "#41b883", "Svelte": "#ff3e00",
}
# Generated, vendored or bundled files. Counting them would credit me with a
# code generator's or a library's output.
GENERATED = re.compile(
    r"(^|/)(node_modules|dist|build|out|bin|obj|vendor|coverage|\.next|wwwroot/lib)/"
    r"|\.min\.(js|css)$|\.designer\.cs$|modelsnapshot\.cs$|(^|/)migrations/.*\.cs$"
    r"|\.g\.cs$|\.generated\.|api-types\.ts$|(^|/)generated/|openapi|\.d\.ts$|lock",
    re.IGNORECASE,
)
# A single file change this large is an import or a paste, not authorship.
MAX_LINES_PER_FILE_CHANGE = 3000
TOP_N = 8


def load_config() -> tuple[set[str], set[str]]:
    if not LOCAL_CONFIG.is_file():
        sys.exit(f"error: {LOCAL_CONFIG} is missing; add one author email per line")
    emails, skip = set(), set()
    for raw in LOCAL_CONFIG.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("skip "):
            skip.add(line[5:].strip())
        else:
            emails.add(line.lower())
    if not emails:
        sys.exit(f"error: no author emails in {LOCAL_CONFIG}")
    return emails, skip


def find_repos(roots: list[Path], exclude: set[str]) -> list[Path]:
    repos = []
    for root in roots:
        if not root.is_dir():
            print(f"warning: {root} does not exist, skipped", file=sys.stderr)
            continue
        for git_dir in root.rglob(".git"):
            repo = git_dir.parent
            if any(part in exclude for part in repo.relative_to(root).parts):
                continue
            if "node_modules" in repo.parts:
                continue
            repos.append(repo)
    return sorted(set(repos))


def count_repo(repo: Path, emails: set[str], seen: set[str], totals: Counter) -> int:
    """Add my lines in one repo to totals. Returns commits counted."""
    # %x00 separates commits; --all covers unmerged branches, and `seen`
    # stops a commit present in two clones from counting twice.
    result = subprocess.run(
        ["git", "-C", str(repo), "log", "--all", "--no-merges", "--no-renames",
         "--numstat", "--format=%x00%H %ae"],
        capture_output=True, text=True, errors="replace",
    )
    if result.returncode != 0:
        print(f"warning: git log failed in {repo}: {result.stderr.strip()[:120]}", file=sys.stderr)
        return 0

    counted = 0
    for block in result.stdout.split("\x00")[1:]:
        header, _, body = block.partition("\n")
        sha, _, email = header.partition(" ")
        if email.lower() not in emails or sha in seen:
            continue
        seen.add(sha)
        counted += 1
        for line in body.splitlines():
            parts = line.split("\t")
            if len(parts) != 3 or not parts[0].isdigit():  # "-" = binary
                continue
            added, path = int(parts[0]), parts[2]
            if added > MAX_LINES_PER_FILE_CHANGE or GENERATED.search(path):
                continue
            language = LANGUAGES.get(Path(path).suffix.lower())
            if language:
                totals[language] += added
    return counted


def render_svg(ranked: list[tuple[str, int]], total: int) -> str:
    width, bar_y, bar_h = 480, 52, 10
    parts, legend, x = [], [], 20.0
    for i, (language, lines) in enumerate(ranked):
        share = lines / total
        w = (width - 40) * share
        colour = COLOURS.get(language, "#8b949e")
        parts.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{w:.2f}" height="{bar_h}" fill="{colour}"/>')
        x += w
        col, row = i % 2, i // 2
        lx, ly = 20 + col * 230, 92 + row * 24
        legend.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{colour}"/>'
            f'<text x="{lx + 16}" y="{ly}" class="t">{language}</text>'
            f'<text x="{lx + 210}" y="{ly}" class="m" text-anchor="end">{share * 100:.1f}%</text>'
        )
    height = 92 + ((len(ranked) + 1) // 2) * 24
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Languages by lines I wrote">
<style>
  .bg {{ fill: #ffffff; stroke: #d0d7de; }} .h {{ fill: #1f2328; }} .t {{ fill: #1f2328; }} .m {{ fill: #59636e; }}
  @media (prefers-color-scheme: dark) {{
    .bg {{ fill: #0d1117; stroke: #30363d; }} .h {{ fill: #e6edf3; }} .t {{ fill: #e6edf3; }} .m {{ fill: #9198a1; }}
  }}
  text {{ font: 13px -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }}
  .h {{ font-weight: 600; font-size: 15px; }}
</style>
<rect class="bg" x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="6"/>
<text x="20" y="34" class="h">Languages I write</text>
<text x="{width - 20}" y="34" class="m" text-anchor="end">by lines authored, all repos</text>
<clipPath id="bar"><rect x="20" y="{bar_y}" width="{width - 40}" height="{bar_h}" rx="5"/></clipPath>
<g clip-path="url(#bar)">{"".join(parts)}</g>
{"".join(legend)}
</svg>
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    emails, exclude = load_config()
    repos = find_repos(ROOTS, exclude)
    seen: set[str] = set()
    totals: Counter = Counter()
    commits = sum(count_repo(repo, emails, seen, totals) for repo in repos)

    total = sum(totals.values())
    if total == 0:
        # Never overwrite a good chart with an empty one.
        print("error: no authored lines found; check authors.local and ROOTS", file=sys.stderr)
        return 1

    ranked = totals.most_common(TOP_N)
    print(f"{len(repos)} repos, {commits} of my commits, {total:,} lines")
    for language, lines in totals.most_common():
        print(f"  {language:<12} {lines:>9,}  {lines / total * 100:5.1f}%")

    if not args.dry_run:
        out = Path(__file__).resolve().parent.parent / "metrics" / "languages.svg"
        out.parent.mkdir(exist_ok=True)
        # Percentages are of the top N only, so the bar fills its width.
        out.write_text(render_svg(ranked, sum(lines for _, lines in ranked)))
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
