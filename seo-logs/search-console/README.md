# Search Console Logs

Run a dated snapshot after meaningful SEO changes or once per week:

```bash
scripts/gsc_tool.py snapshot --site-url sc-domain:vedica-ayurveda.co.il
```

The command writes:

- `gsc-snapshot.json` with raw Search Console API data.
- `summary.md` with top pages, week-over-week comparison, top query/page pairs, and index inspection for tracked URLs.

Search Console performance data is delayed, so use logs from 7-14 days after a change to judge ranking impact.
