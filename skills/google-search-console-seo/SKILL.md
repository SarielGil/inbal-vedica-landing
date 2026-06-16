---
name: google-search-console-seo
description: Diagnose Google indexing, Search Console, sitemap, hreflang, canonical, SERP regression, and SEO/AEO page-readiness issues. Use when a user asks why pages are not found in Google, whether SEO results degraded, how to request indexing, run an SEO/AEO test, compare live pages with indexed/search results, or check page answerability for search and AI surfaces.
---

# Google Search Console SEO

Use this skill to separate problems that often get confused: crawlability, indexing, ranking, snippet/search visibility, and answerability for AI/search surfaces.

Prefer an efficient evidence trail over a long audit: live URL checks, Search Console facts, a few representative live-search queries, local HTML/schema checks, and a saved report when the user wants a record.

## Workflow

1. Identify the page set and intent.
- For multilingual service pages, test both the local-language page and its English/alternate page when relevant.
- Classify the target intent: brand/entity, service discovery, local search, tour/event, article, or support page.
- Preserve structured entity identity, but make broad discovery surfaces service-first unless the user explicitly wants branded/name-led SEO.

2. Check the live URL first.
- Confirm `200 OK` with `curl -sIL`.
- Confirm no `noindex` in HTML or `X-Robots-Tag`.
- Confirm canonical points to the intended URL.
- Confirm robots.txt allows the page.
- Confirm the page is present in sitemap.xml with a current `lastmod`.
- For alternate-language pages, confirm reciprocal `hreflang` in page HTML and sitemap.
- Confirm the page has at least one crawlable internal link from an important page, not only sitemap/hreflang.

3. Check local SEO/AEO readiness.
- Extract and record: title length, meta description length, robots meta, canonical, H1 count/text, H2 topics, image alt coverage, internal/external link counts.
- Parse all JSON-LD. Record schema types and any parse errors.
- For AEO, verify direct answer blocks for likely questions: what it is, who it is for, location, language, process, preparation/booking, limitations/caveats, and how to contact.
- For medical/wellness pages, confirm complementary-care caveats are present and avoid unsupported claims.
- For discovery queries, avoid overusing a specific person name in titles, descriptions, hero copy, generic alt text, service descriptions, and footer/site-name labels. Keep the person name in `Person` schema, author/about/profile/review contexts, and external trust references.

4. Compare deployed HTML with search results.
- Check the live `<title>`, meta description, `h1`, canonical, and visible internal links.
- Search exact URL and `site:domain/path` when browsing is available.
- Search 2-4 representative query types:
  - exact URL or `site:` query
  - entity-rich query
  - service + location query
  - broad/generic query if relevant
- Record whether the page appears and which competitors/directories surface.
- Treat stale SERP titles/snippets as possible indexing lag until Search Console proves otherwise.

5. Use Search Console if available.
- Inspect the URL.
- Record: indexing status, last crawl date, user-declared canonical, Google-selected canonical, referring page, sitemap discovery, and mobile usability.
- Record rich-result verdicts and detected items when present.
- Request indexing for important newly published or recently fixed pages.
- Resubmit sitemap after publishing batches of priority URLs.
- Check Performance for query, page, country, device, date range, clicks, impressions, CTR, and average position.
- For page tests, use a stable window such as the last 28 complete days, then compare the current 7 complete days to the previous 7 complete days.
- Query/page rows may be privacy-thinned on low-volume pages. Always also check page-only totals.

6. Save a compact report when useful.
- Use `seo-logs/aeo-live-search/YYYY-MM-DD-page-slug.md` for SEO/AEO page tests.
- Include: scope, whether Google Custom Search API was actually available, Search Console indexing, 28-day performance, week comparison, live search visibility, on-page SEO, AEO readiness, and recommendations.
- If Google Custom Search JSON API credentials are missing, state that clearly and use live web search plus Search Console instead. Do not claim a CSE API test ran without `GOOGLE_API_KEY` and CSE `cx`/`GOOGLE_CSE_ID`.

7. Before pushing SEO or content changes.
- Update `sitemap.xml` `lastmod` dates for changed priority URLs only.
- Validate sitemap XML, for example `xmllint --noout sitemap.xml` when available.
- Confirm changed URLs are listed in the sitemap and that multilingual pages have reciprocal page-level and sitemap `hreflang`.
- If Search Console is available, submit the sitemap after deployment and inspect key changed URLs.
- Record sitemap submission, coverage state, canonical, last crawl date and any rich-result warnings in the work summary.
- If changes are only pushed to a branch and not deployed, say that GSC still sees the live sitemap/pages and may report stale dates or old schema.
- Do not describe API sitemap submission as a manual "Request indexing"; that button is available in the Search Console UI.

8. If Search Console is not available.
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
- Do not remove all entity/person references from trust surfaces just because service-first SEO is desired. Reduce name dependence in discovery copy; preserve entity disambiguation in schema and proof contexts.

## Efficient Local Commands

Use the project helper if present:

```bash
python3 scripts/gsc_tool.py inspect https://example.com/page.html --site-url sc-domain:example.com
python3 scripts/gsc_tool.py performance --site-url sc-domain:example.com --start-date YYYY-MM-DD --end-date YYYY-MM-DD --dimensions page --page https://example.com/page.html --row-limit 10
python3 scripts/gsc_tool.py performance --site-url sc-domain:example.com --start-date YYYY-MM-DD --end-date YYYY-MM-DD --dimensions query,page --page https://example.com/page.html --row-limit 50
```

If using the global helper:

```bash
python3 ~/.codex/skills/google-search-console/scripts/gsc.py inspect https://example.com/page.html --site-url sc-domain:example.com
```

For local HTML/schema checks, prefer a small parser script over regex-only scraping. Check:

- title/meta description length
- canonical/robots
- H1/H2 structure
- image alt coverage
- JSON-LD parse errors and schema types
- direct answer blocks and medical/complementary-care caveats

Run the repo guard when available:

```bash
npm run check:external-tags
```

## Reporting Template

- **Crawlability:** status code, robots, noindex, canonical.
- **Discovery:** sitemap, internal links, hreflang.
- **Indexing:** Search Console URL Inspection result, if available.
- **Ranking:** Search Console query/page comparison, if available.
- **Live search:** exact URL/site query, entity query, service/location query, and broad query competitors.
- **On-page SEO:** title, description, H1, schema, alt text, internal links.
- **AEO readiness:** direct answers, FAQ/schema alignment, contact/booking clarity, caveats.
- **Sitemap/recrawl:** `lastmod` changes, XML validation, sitemap submission status, live-vs-branch caveat.
- **Action:** what was fixed, what needs manual GSC action, and when to re-check.
