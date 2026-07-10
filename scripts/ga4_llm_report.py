#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path


DEFAULT_LLM_SOURCES = [
    "chatgpt",
    "openai",
    "perplexity",
    "claude",
    "gemini",
    "bard",
    "copilot",
    "poe",
    "you.com",
    "phind",
    "mistral",
    "meta.ai",
    "deepseek",
    "grok",
]


def load_ga4_types():
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange,
            Dimension,
            Filter,
            FilterExpression,
            FilterExpressionList,
            Metric,
            RunReportRequest,
        )
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing GA4 Data API package. Install it with:\n"
            "  python3 -m pip install --user google-analytics-data"
        ) from exc

    return {
        "BetaAnalyticsDataClient": BetaAnalyticsDataClient,
        "DateRange": DateRange,
        "Dimension": Dimension,
        "Filter": Filter,
        "FilterExpression": FilterExpression,
        "FilterExpressionList": FilterExpressionList,
        "Metric": Metric,
        "RunReportRequest": RunReportRequest,
    }


def source_filter(types, sources):
    expressions = []
    for source in sources:
        expressions.append(
            types["FilterExpression"](
                filter=types["Filter"](
                    field_name="sessionSource",
                    string_filter=types["Filter"].StringFilter(
                        match_type=types["Filter"].StringFilter.MatchType.CONTAINS,
                        value=source,
                        case_sensitive=False,
                    ),
                )
            )
        )
    return types["FilterExpression"](
        or_group=types["FilterExpressionList"](expressions=expressions)
    )


def event_filter(types, event_name):
    return types["FilterExpression"](
        filter=types["Filter"](
            field_name="eventName",
            string_filter=types["Filter"].StringFilter(
                match_type=types["Filter"].StringFilter.MatchType.EXACT,
                value=event_name,
            ),
        )
    )


def run_report(client, types, property_id, dimensions, metrics, start_date, end_date, dimension_filter=None, limit=1000):
    request = types["RunReportRequest"](
        property=f"properties/{property_id}",
        dimensions=[types["Dimension"](name=name) for name in dimensions],
        metrics=[types["Metric"](name=name) for name in metrics],
        date_ranges=[types["DateRange"](start_date=start_date, end_date=end_date)],
        dimension_filter=dimension_filter,
        limit=limit,
    )
    return client.run_report(request)


def rows_to_dicts(response):
    headers = [header.name for header in response.dimension_headers] + [
        header.name for header in response.metric_headers
    ]
    rows = []
    for row in response.rows:
        values = [value.value for value in row.dimension_values] + [
            value.value for value in row.metric_values
        ]
        rows.append(dict(zip(headers, values)))
    return rows


def print_table(title, rows, columns):
    print(f"\n## {title}")
    if not rows:
        print("No rows returned.")
        return
    print("| " + " | ".join(columns) + " |")
    print("|" + "|".join(["---"] * len(columns)) + "|")
    for row in rows:
        print("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")


def save_json(path, data):
    if not path:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved {out}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Report Vedica GA4 LLM referral history and new LLM referral events."
    )
    parser.add_argument("--property-id", default=os.environ.get("GA4_PROPERTY_ID"), help="Numeric GA4 property ID.")
    parser.add_argument("--credentials", help="Path to service-account JSON. Sets GOOGLE_APPLICATION_CREDENTIALS.")
    parser.add_argument("--start-date", default="2026-06-01")
    parser.add_argument("--end-date", default="yesterday")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--save-json", help="Optional output JSON path.")
    parser.add_argument(
        "--llm-source",
        action="append",
        dest="llm_sources",
        help="Additional source substring to match in sessionSource. Can be repeated.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.property_id:
        raise SystemExit(
            "Missing numeric GA4 property ID. Pass --property-id or set GA4_PROPERTY_ID.\n"
            "In GA4: Admin -> Property details -> Property ID."
        )
    if args.credentials:
        credentials_path = Path(args.credentials).expanduser()
        if not credentials_path.exists():
            raise SystemExit(
                f"Credential file not found: {credentials_path}\n"
                "Create/download the GA4 service-account JSON and save it there, "
                "or pass the correct --credentials path."
            )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise SystemExit(
            "Missing credentials. Set GOOGLE_APPLICATION_CREDENTIALS or pass --credentials "
            "with a service-account JSON path."
        )

    types = load_ga4_types()
    client = types["BetaAnalyticsDataClient"]()
    sources = DEFAULT_LLM_SOURCES + (args.llm_sources or [])

    referral_response = run_report(
        client=client,
        types=types,
        property_id=args.property_id,
        dimensions=["date", "sessionSource", "sessionMedium"],
        metrics=["sessions", "activeUsers", "eventCount"],
        start_date=args.start_date,
        end_date=args.end_date,
        dimension_filter=source_filter(types, sources),
        limit=args.limit,
    )
    referral_rows = rows_to_dicts(referral_response)

    event_response = run_report(
        client=client,
        types=types,
        property_id=args.property_id,
        dimensions=["date", "eventName"],
        metrics=["eventCount", "activeUsers"],
        start_date=args.start_date,
        end_date=args.end_date,
        dimension_filter=event_filter(types, "llm_referral_visit"),
        limit=args.limit,
    )
    event_rows = rows_to_dicts(event_response)

    print(f"GA4 property: {args.property_id}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    print_table(
        "Historical LLM-Like Referral Sessions",
        referral_rows,
        ["date", "sessionSource", "sessionMedium", "sessions", "activeUsers", "eventCount"],
    )
    print_table(
        "New llm_referral_visit Events",
        event_rows,
        ["date", "eventName", "eventCount", "activeUsers"],
    )

    save_json(
        args.save_json,
        {
            "property_id": args.property_id,
            "date_range": {"start_date": args.start_date, "end_date": args.end_date},
            "historical_llm_like_referral_sessions": referral_rows,
            "new_llm_referral_visit_events": event_rows,
        },
    )


if __name__ == "__main__":
    main()
