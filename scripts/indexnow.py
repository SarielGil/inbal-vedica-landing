#!/usr/bin/env python3
"""Notify IndexNow after the changed public files have been deployed.

The verification key is a public file, not an account credential. This tool
does not need Bing Webmaster Tools access and does not guarantee indexing.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.indexnow.org/indexnow"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def site_url(host, path):
    return "https://" + host + ("/" if path == "index.html" else "/" + urllib.parse.quote(path))


def changed_files(since, until):
    # Reject options and resolve refs before using them in a diff.
    refs = []
    for ref in (since, until):
        refs.append(git("rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip())
    # Disable rename detection so both old and new URL paths are notified.
    output = git("diff", "--no-renames", "--name-only", "-z", *refs, "--")
    return [p.decode() for p in output.split(b"\0") if p]


def sitemap_pages(xml):
    root = ET.fromstring(xml)
    pages = set()
    for loc in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        path = urllib.parse.urlsplit(loc.text).path.lstrip("/") or "index.html"
        if path.endswith(".html") and "/" not in path:
            pages.add(path)
    return pages


def select_urls(host, paths, previous_pages=None):
    public = sitemap_pages((ROOT / "sitemap.xml").read_text()) | (previous_pages or set())
    pages = set(paths) & public
    # Changes to shared styles, scripts, and media can affect existing pages.
    assets = {p for p in paths if p.startswith("assets/") or p in {"style.css", "script.js", "content.json"}}
    if assets:
        for name in public:
            page = ROOT / name
            if page.exists() and any(asset in page.read_text(encoding="utf-8") for asset in assets):
                pages.add(name)
    return sorted(site_url(host, p) for p in pages)


def validate_url(host, url):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != host or parsed.query or parsed.fragment
            or (parsed.path != "/" and not re.fullmatch(r"/[A-Za-z0-9_-]+\.html", parsed.path))):
        raise ValueError("Expected a canonical HTTPS page on " + host + ": " + url)
    return url


def expected_files(host, urls, key_file):
    files = {"https://" + host + "/" + key_file: (ROOT / key_file).read_bytes()}
    for url in urls:
        name = urllib.parse.unquote(urllib.parse.urlsplit(url).path).lstrip("/") or "index.html"
        path = ROOT / name
        # None means a removed page; deployment must return 404 or 410.
        files[url] = path.read_bytes() if path.exists() else None
    return files


def deployment_ready(files):
    pending = []
    for url, expected in files.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Vedica-IndexNow/1.0", "Cache-Control": "no-cache"})
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                actual = response.read()
                if expected is None or response.geturl() != url or hashlib.sha256(actual).digest() != hashlib.sha256(expected).digest():
                    pending.append(url)
        except urllib.error.HTTPError as exc:
            if expected is not None or exc.code not in (404, 410):
                pending.append(url)
        except (OSError, TimeoutError):
            pending.append(url)
    return pending


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", help="Submit public pages changed since this git commit")
    parser.add_argument("--until", default="HEAD", help="End commit for change discovery")
    parser.add_argument("--url", action="append", default=[], help="A newly changed canonical page; repeat as needed")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without network requests")
    parser.add_argument("--wait-seconds", type=int, default=0, help="Wait for deployment before notifying IndexNow")
    args = parser.parse_args(argv)
    config = json.loads((ROOT / "indexnow.json").read_text())
    host, key_file = config["host"], config["keyFile"]
    if host != "vedica-ayurveda.co.il" or not re.fullmatch(r"[a-f0-9]{32}\.txt", key_file):
        parser.error("Unexpected host or key file in indexnow.json")
    key = (ROOT / key_file).read_text().strip()
    if key + ".txt" != key_file:
        parser.error("Key file name and contents do not match")
    if args.wait_seconds < 0:
        parser.error("--wait-seconds must be nonnegative")
    if not args.since and not args.url:
        parser.error("Provide --since or at least one --url; historical sitemap bulk submission is intentionally unsupported")
    paths = changed_files(args.since, args.until) if args.since else []
    previous_pages = sitemap_pages(git("show", args.since + ":sitemap.xml")) if args.since else set()
    urls = sorted(set(select_urls(host, paths, previous_pages) + [validate_url(host, url) for url in args.url]))
    for url in urls:
        validate_url(host, url)
    if not urls:
        print("No changed public pages to notify.")
        return 0
    if len(urls) > 10000:
        parser.error("IndexNow accepts at most 10,000 URLs per request")
    payload = {"host": host, "key": key, "keyLocation": "https://" + host + "/" + key_file, "urlList": urls}
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0
    files = expected_files(host, urls, key_file)
    deadline = time.monotonic() + args.wait_seconds
    while True:
        pending = deployment_ready(files)
        if not pending:
            break
        if time.monotonic() >= deadline:
            raise RuntimeError("Deployment does not yet match local files: " + ", ".join(pending))
        print("Waiting for deployment: " + ", ".join(pending), flush=True)
        time.sleep(min(15, max(0, deadline - time.monotonic())))
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            body = response.read().decode()
    except urllib.error.HTTPError as exc:
        raise RuntimeError("IndexNow returned HTTP " + str(exc.code) + ": " + exc.read().decode()) from exc
    if status not in (200, 202):
        raise RuntimeError("Unexpected IndexNow status: " + str(status))
    print(json.dumps({"status": status, "urls": urls, "message": "Received; key validation pending" if status == 202 else "Received", "response": body}, indent=2))
    print("Receipt confirms notification, not crawling, indexing, ranking, or AI citations.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
