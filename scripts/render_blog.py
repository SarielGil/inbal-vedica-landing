#!/usr/bin/env python3
"""Render crawlable blog cards. Run after editing blog-data.json; --check is for CI."""

import argparse
import datetime as dt
from html import escape
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
START = "        <!-- blog-posts:start -->"
END = "        <!-- blog-posts:end -->"


def render_posts(posts):
    cards = []
    seen = set()
    posts = sorted(posts, key=lambda post: (bool(post.get("featured")), post["date"]), reverse=True)
    for post in posts:
        slug = post["slug"]
        if not re.fullmatch(r"[a-z0-9-]+", slug) or slug in seen:
            raise ValueError(f"Invalid or duplicate blog slug: {slug}")
        if not (ROOT / f"{slug}.html").is_file():
            raise ValueError(f"Missing article: {slug}.html")
        seen.add(slug)
        date = dt.date.fromisoformat(post["date"])
        featured = " blog-card--featured" if post.get("featured") else ""
        category, title, excerpt = (escape(post[key], quote=True) for key in ("category", "title", "excerpt"))
        cards.append(f'''            <article class="blog-card{featured}" data-category="{category}">
                <div class="blog-card__body">
                    <div class="blog-card__meta">
                        <span class="blog-card__category">{category}</span>
                        <time class="blog-card__date" datetime="{date.isoformat()}">{date.strftime('%d.%m.%Y')}</time>
                    </div>
                    <h2><a href="{slug}.html">{title}</a></h2>
                    <p class="blog-card__excerpt">{excerpt}</p>
                    <a href="{slug}.html" class="blog-card__link">לקריאת המדריך</a>
                </div>
            </article>''')
    return '\n'.join([START, '        <div id="posts-container" class="blog-grid">', *cards, '        </div>', END])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    posts = json.loads((ROOT / "blog-data.json").read_text(encoding="utf-8"))["posts"]
    path = ROOT / "blog.html"
    source = path.read_text(encoding="utf-8")
    if source.count(START) != 1 or source.count(END) != 1:
        raise SystemExit("Expected one blog-posts:start/end marker pair in blog.html")
    start = source.index(START)
    end = source.index(END, start) + len(END)
    rendered = source[:start] + render_posts(posts) + source[end:]
    if args.check:
        if source != rendered:
            raise SystemExit("Blog cards are stale. Run npm run build:blog and include blog.html.")
        print(f"Blog cards match blog-data.json: {len(posts)} crawlable articles.")
    else:
        path.write_text(rendered, encoding="utf-8")
        print(f"Rendered {len(posts)} blog cards into blog.html.")


if __name__ == "__main__":
    main()
