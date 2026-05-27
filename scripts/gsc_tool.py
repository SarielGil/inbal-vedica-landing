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
DEFAULT_SITEMAP_URL = "https://vedica-ayurveda.co.il/sitemap.xml"
CONFIG_DIR = Path.home() / ".config" / "vedica-gsc"
TOKEN_PATH = CONFIG_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]


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
    if args.submit:
        svc.sitemaps().submit(siteUrl=args.site_url, feedpath=args.sitemap_url).execute()
        print(f"Submitted {args.sitemap_url} for {args.site_url}")
        return
    print_json(svc.sitemaps().list(siteUrl=args.site_url).execute())


def cmd_performance(args):
    svc = service()
    end_date = args.end_date or dt.date.today().isoformat()
    start_date = args.start_date or (dt.date.fromisoformat(end_date) - dt.timedelta(days=28)).isoformat()
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": args.dimensions.split(","),
        "rowLimit": args.row_limit,
    }
    if args.page:
        body["dimensionFilterGroups"] = [{
            "filters": [{
                "dimension": "page",
                "operator": "equals",
                "expression": args.page,
            }]
        }]
    print_json(svc.searchanalytics().query(siteUrl=args.site_url, body=body).execute())


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
    sitemaps.add_argument("--sitemap-url", default=DEFAULT_SITEMAP_URL)
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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
