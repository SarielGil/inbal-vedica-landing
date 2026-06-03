---
name: google-search-console-seo
description: Diagnose Google indexing, Search Console, sitemap, hreflang, canonical, and SERP regression issues. Use when a user asks why pages are not found in Google, whether SEO results degraded, how to request indexing, or how to compare live pages with indexed/search results.
---

# Google Search Console SEO

Use this skill to separate three different problems that often get confused: crawlability, indexing, and ranking.

## Workflow

1. Check the live URL first.
- Confirm `200 OK` with `curl -sIL`.
- Confirm no `noindex` in HTML or `X-Robots-Tag`.
- Confirm canonical points to the intended URL.
- Confirm robots.txt allows the page.
- Confirm the page is present in sitemap.xml with a current `lastmod`.
- For alternate-language pages, confirm reciprocal `hreflang` in page HTML and sitemap.
- Confirm the page has at least one crawlable internal link from an important page, not only sitemap/hreflang.

2. Compare deployed HTML with search results.
- Check the live `<title>`, meta description, `h1`, canonical, and visible internal links.
- Search exact URL and `site:domain/path` when browsing is available.
- Treat stale SERP titles/snippets as possible indexing lag until Search Console proves otherwise.

3. Use Search Console if available.
- Inspect the URL.
- Record: indexing status, last crawl date, user-declared canonical, Google-selected canonical, referring page, sitemap discovery, and mobile usability.
- Request indexing for important newly published or recently fixed pages.
- Resubmit sitemap after publishing batches of priority URLs.
- Check Performance for query, page, country, device, date range, clicks, impressions, CTR, and average position.

4. Before pushing SEO or content changes.
- Update `sitemap.xml` `lastmod` dates for changed priority URLs only.
- Validate sitemap XML, for example `xmllint --noout sitemap.xml` when available.
- Confirm changed URLs are listed in the sitemap and that multilingual pages have reciprocal page-level and sitemap `hreflang`.
- If Search Console is available, submit the sitemap after deployment and inspect key changed URLs.
- Record sitemap submission, coverage state, canonical, last crawl date and any rich-result warnings in the work summary.
- If changes are only pushed to a branch and not deployed, say that GSC still sees the live sitemap/pages and may report stale dates or old schema.
- Do not describe API sitemap submission as a manual "Request indexing"; that button is available in the Search Console UI.

5. If Search Console is not available.
- Give the user a manual checklist:
  - URL Inspection -> inspect exact URL.
  - Test Live URL.
  - Request Indexing.
  - Sitemaps -> resubmit `https://example.com/sitemap.xml`.
  - Performance -> compare last 7/28 days with previous period.

## Regression Guardrails

- Do not call a page "not indexed" only because it does not rank yet.
- Do not call SEO degraded without comparing dates, query set, country/device, and Search Console impressions.
- New pages can be crawlable but absent from Google for days or weeks on small sites.
- Preserve working exact-match titles/H1s unless the new query target is explicit.
- Internal links from homepage, nav, footer, and relevant service pages matter more than sitemap-only discovery.

## Reporting Template

- **Crawlability:** status code, robots, noindex, canonical.
- **Discovery:** sitemap, internal links, hreflang.
- **Indexing:** Search Console URL Inspection result, if available.
- **Ranking:** Search Console query/page comparison, if available.
- **Sitemap/recrawl:** `lastmod` changes, XML validation, sitemap submission status, live-vs-branch caveat.
- **Action:** what was fixed, what needs manual GSC action, and when to re-check.
