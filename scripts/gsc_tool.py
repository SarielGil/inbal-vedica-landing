#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


DEFAULT_SITE_URL = "https://vedica-ayurveda.co.il/"
CONFIG_DIR = Path.home() / ".config" / "vedica-gsc"
TOKEN_PATH = CONFIG_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]
DEFAULT_TRACKED_URLS = [
    "https://vedica-ayurveda.co.il/",
    "https://vedica-ayurveda.co.il/clinic.html",
    "https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html",
    "https://vedica-ayurveda.co.il/persian-medicine.html",
    "https://vedica-ayurveda.co.il/tours.html",
    "https://vedica-ayurveda.co.il/levinsky-market-food-tour.html",
    "https://vedica-ayurveda.co.il/workshops.html",
]


def load_credentials(client_secret=None, interactive=False):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not interactive:
            raise SystemExit(
                "Not authenticated. Run: scripts/gsc_tool.py auth --client-secret /path/to/client_secret.json"
            )
        if not client_secret:
            raise SystemExit("--client-secret is required for first auth")
        flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)

    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    os.chmod(TOKEN_PATH, 0o600)
    return creds


def service(client_secret=None, interactive=False):
    creds = load_credentials(client_secret=client_secret, interactive=interactive)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def default_sitemap_for_site(site_url):
    if site_url.startswith("sc-domain:"):
        domain = site_url.split(":", 1)[1].strip("/")
        return f"https://{domain}/sitemap.xml"
    return site_url.rstrip("/") + "/sitemap.xml"


def cmd_auth(args):
    load_credentials(client_secret=args.client_secret, interactive=True)
    print(f"Authenticated. Token stored at {TOKEN_PATH}")


def cmd_sites(args):
    svc = service()
    print_json(svc.sites().list().execute())


def cmd_inspect(args):
    svc = service()
    body = {"inspectionUrl": args.url, "siteUrl": args.site_url}
    print_json(svc.urlInspection().index().inspect(body=body).execute())


def cmd_sitemaps(args):
    svc = service()
    sitemap_url = args.sitemap_url or default_sitemap_for_site(args.site_url)
    if args.submit:
        svc.sitemaps().submit(siteUrl=args.site_url, feedpath=sitemap_url).execute()
        print(f"Submitted {sitemap_url} for {args.site_url}")
        return
    print_json(svc.sitemaps().list(siteUrl=args.site_url).execute())


def cmd_performance(args):
    svc = service()
    end_date = args.end_date or dt.date.today().isoformat()
    start_date = args.start_date or (dt.date.fromisoformat(end_date) - dt.timedelta(days=28)).isoformat()
    print_json(query_performance(svc, args.site_url, start_date, end_date, args.dimensions.split(","), args.row_limit, page=args.page))


def query_performance(svc, site_url, start_date, end_date, dimensions, row_limit, page=None):
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    if page:
        body["dimensionFilterGroups"] = [{
            "filters": [{
                "dimension": "page",
                "operator": "equals",
                "expression": page,
            }]
        }]
    return svc.searchanalytics().query(siteUrl=site_url, body=body).execute()


def inspect_url(svc, site_url, url):
    body = {"inspectionUrl": url, "siteUrl": site_url}
    return svc.urlInspection().index().inspect(body=body).execute()


def summarize_rows(rows, max_rows=12):
    if not rows:
        return ["No rows returned."]
    lines = ["| Item | Clicks | Impressions | CTR | Avg position |", "|---|---:|---:|---:|---:|"]
    for row in rows[:max_rows]:
        key = " / ".join(row.get("keys", [""]))
        ctr = row.get("ctr", 0) * 100
        lines.append(
            f"| {key} | {row.get('clicks', 0)} | {row.get('impressions', 0)} | {ctr:.1f}% | {row.get('position', 0):.2f} |"
        )
    return lines


def row_by_page(rows):
    out = {}
    for row in rows:
        keys = row.get("keys", [])
        if keys:
            out[keys[0]] = row
    return out


def compare_page_rows(current_rows, previous_rows, max_rows=12):
    current = row_by_page(current_rows)
    previous = row_by_page(previous_rows)
    pages = sorted(set(current) | set(previous))
    if not pages:
        return ["No rows returned."]
    lines = [
        "| Page | Clicks | Prev clicks | Impr. | Prev impr. | Pos. | Prev pos. |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    pages = sorted(
        pages,
        key=lambda p: (
            current.get(p, {}).get("clicks", 0) + previous.get(p, {}).get("clicks", 0),
            current.get(p, {}).get("impressions", 0) + previous.get(p, {}).get("impressions", 0),
        ),
        reverse=True,
    )
    for page in pages[:max_rows]:
        c = current.get(page, {})
        p = previous.get(page, {})
        current_pos = f"{c.get('position', 0):.2f}" if c else "-"
        previous_pos = f"{p.get('position', 0):.2f}" if p else "-"
        lines.append(
            f"| {page} | {c.get('clicks', 0)} | {p.get('clicks', 0)} | "
            f"{c.get('impressions', 0)} | {p.get('impressions', 0)} | "
            f"{current_pos} | {previous_pos} |"
        )
    return lines


def cmd_snapshot(args):
    svc = service()
    snapshot_date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    end_date = args.end_date or (snapshot_date - dt.timedelta(days=1)).isoformat()
    end = dt.date.fromisoformat(end_date)
    start = end - dt.timedelta(days=args.lookback_days - 1)
    current_start = end - dt.timedelta(days=args.compare_days - 1)
    previous_end = current_start - dt.timedelta(days=1)
    previous_start = previous_end - dt.timedelta(days=args.compare_days - 1)

    tracked_urls = args.url or DEFAULT_TRACKED_URLS
    page_lookback = query_performance(
        svc, args.site_url, start.isoformat(), end.isoformat(), ["page"], args.row_limit
    )
    query_page_lookback = query_performance(
        svc, args.site_url, start.isoformat(), end.isoformat(), ["query", "page"], args.row_limit
    )
    current_pages = query_performance(
        svc, args.site_url, current_start.isoformat(), end.isoformat(), ["page"], args.row_limit
    )
    previous_pages = query_performance(
        svc, args.site_url, previous_start.isoformat(), previous_end.isoformat(), ["page"], args.row_limit
    )
    inspections = {}
    if not args.skip_inspection:
        for url in tracked_urls:
            try:
                inspections[url] = inspect_url(svc, args.site_url, url)
            except Exception as exc:
                inspections[url] = {"error": str(exc)}

    snapshot = {
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "site_url": args.site_url,
        "lookback_range": {"start_date": start.isoformat(), "end_date": end.isoformat()},
        "current_compare_range": {"start_date": current_start.isoformat(), "end_date": end.isoformat()},
        "previous_compare_range": {"start_date": previous_start.isoformat(), "end_date": previous_end.isoformat()},
        "tracked_urls": tracked_urls,
        "performance": {
            "pages": page_lookback,
            "queries_pages": query_page_lookback,
            "current_pages": current_pages,
            "previous_pages": previous_pages,
        },
        "inspections": inspections,
    }

    output_dir = Path(args.output_dir) / snapshot_date.isoformat()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "gsc-snapshot.json"
    md_path = output_dir / "summary.md"
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    md = [
        f"# Search Console Snapshot - {snapshot_date.isoformat()}",
        "",
        f"- Site: `{args.site_url}`",
        f"- Lookback: `{start.isoformat()}` to `{end.isoformat()}`",
        f"- Compare current: `{current_start.isoformat()}` to `{end.isoformat()}`",
        f"- Compare previous: `{previous_start.isoformat()}` to `{previous_end.isoformat()}`",
        "",
        "## Top Pages",
        *summarize_rows(page_lookback.get("rows", [])),
        "",
        "## Week Comparison",
        *compare_page_rows(current_pages.get("rows", []), previous_pages.get("rows", [])),
        "",
        "## Top Queries By Page",
        *summarize_rows(query_page_lookback.get("rows", []), max_rows=20),
        "",
        "## Index Inspection",
    ]
    for url, result in inspections.items():
        status = result.get("inspectionResult", {}).get("indexStatusResult", {})
        md.append(
            f"- `{url}`: {status.get('coverageState', result.get('error', 'unknown'))}; "
            f"canonical `{status.get('googleCanonical', 'unknown')}`; "
            f"last crawl `{status.get('lastCrawlTime', 'unknown')}`"
        )
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


def main():
    parser = argparse.ArgumentParser(description="Google Search Console helper for VEDICA.")
    sub = parser.add_subparsers(required=True)

    auth = sub.add_parser("auth", help="Authenticate with OAuth and store a local token.")
    auth.add_argument("--client-secret", required=True)
    auth.set_defaults(func=cmd_auth)

    sites = sub.add_parser("sites", help="List Search Console sites available to this account.")
    sites.set_defaults(func=cmd_sites)

    inspect = sub.add_parser("inspect", help="Inspect Google indexed status for one URL.")
    inspect.add_argument("url")
    inspect.add_argument("--site-url", default=DEFAULT_SITE_URL)
    inspect.set_defaults(func=cmd_inspect)

    sitemaps = sub.add_parser("sitemaps", help="List or submit sitemaps.")
    sitemaps.add_argument("--site-url", default=DEFAULT_SITE_URL)
    sitemaps.add_argument("--sitemap-url")
    sitemaps.add_argument("--submit", action="store_true")
    sitemaps.set_defaults(func=cmd_sitemaps)

    perf = sub.add_parser("performance", help="Query Search Console performance data.")
    perf.add_argument("--site-url", default=DEFAULT_SITE_URL)
    perf.add_argument("--start-date")
    perf.add_argument("--end-date")
    perf.add_argument("--dimensions", default="query,page")
    perf.add_argument("--row-limit", type=int, default=25)
    perf.add_argument("--page")
    perf.set_defaults(func=cmd_performance)

    snapshot = sub.add_parser("snapshot", help="Write a dated Search Console performance and indexing log.")
    snapshot.add_argument("--site-url", default="sc-domain:vedica-ayurveda.co.il")
    snapshot.add_argument("--date", help="Snapshot date, YYYY-MM-DD. Defaults to today.")
    snapshot.add_argument("--end-date", help="GSC data end date, YYYY-MM-DD. Defaults to snapshot date minus 1 day.")
    snapshot.add_argument("--lookback-days", type=int, default=28)
    snapshot.add_argument("--compare-days", type=int, default=7)
    snapshot.add_argument("--row-limit", type=int, default=100)
    snapshot.add_argument("--output-dir", default="seo-logs/search-console")
    snapshot.add_argument("--url", action="append", help="Tracked URL to inspect. Can be passed multiple times.")
    snapshot.add_argument("--skip-inspection", action="store_true")
    snapshot.set_defaults(func=cmd_snapshot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
