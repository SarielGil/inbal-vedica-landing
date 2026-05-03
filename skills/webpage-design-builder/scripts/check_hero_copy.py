#!/usr/bin/env python3
"""Quick hero-copy lint for static HTML pages.

Checks first <h1> and first <p> after it against word-count thresholds.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Optional

H1_PATTERN = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
P_PATTERN = re.compile(r"<p[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")


def clean_text(raw: str) -> str:
    text = TAG_PATTERN.sub(" ", raw)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    return SPACE_PATTERN.sub(" ", text).strip()


def count_words(text: str) -> int:
    if not text:
        return 0
    return len([w for w in text.split(" ") if w])


def extract_first_h1(content: str) -> str:
    match = H1_PATTERN.search(content)
    return clean_text(match.group(1)) if match else ""


def extract_first_subtitle(content: str, h1_end: Optional[int]) -> str:
    search_start = h1_end if h1_end is not None else 0
    match = P_PATTERN.search(content, pos=search_start)
    return clean_text(match.group(1)) if match else ""


def lint_file(path: pathlib.Path, h1_max: int, subtitle_max: int) -> list[str]:
    content = path.read_text(encoding="utf-8", errors="ignore")

    h1_match = H1_PATTERN.search(content)
    h1 = clean_text(h1_match.group(1)) if h1_match else ""
    subtitle = extract_first_subtitle(content, h1_match.end() if h1_match else None)

    issues: list[str] = []

    if not h1:
        issues.append("missing h1")
    else:
        h1_words = count_words(h1)
        if h1_words > h1_max:
            issues.append(f"h1 too long ({h1_words}>{h1_max}): {h1}")

    if subtitle:
        subtitle_words = count_words(subtitle)
        if subtitle_words > subtitle_max:
            issues.append(
                f"subtitle too long ({subtitle_words}>{subtitle_max}): {subtitle}"
            )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint hero copy density in HTML files")
    parser.add_argument("files", nargs="*", help="HTML files to check")
    parser.add_argument("--h1-max", type=int, default=10, help="Max words for h1")
    parser.add_argument(
        "--subtitle-max", type=int, default=18, help="Max words for first subtitle paragraph"
    )
    args = parser.parse_args()

    files = [pathlib.Path(f) for f in args.files] if args.files else sorted(pathlib.Path(".").glob("*.html"))

    if not files:
        print("No HTML files found.")
        return 0

    has_issues = False
    for file_path in files:
        if not file_path.is_file():
            print(f"[SKIP] {file_path} (not found)")
            continue

        issues = lint_file(file_path, args.h1_max, args.subtitle_max)
        if issues:
            has_issues = True
            print(f"[WARN] {file_path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[OK] {file_path}")

    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
