# SEO/AEO Live Search Check - Levinsky Market Food Tour

Date: 2026-06-16
Page: https://vedica-ayurveda.co.il/levinsky-market-food-tour.html

## Google Custom Search API

Google Custom Search JSON API was not run because no local API key or CSE `cx` ID was found in the repo or environment.

Commands/checks used instead:
- Google Search Console snapshot via `scripts/gsc_tool.py`
- Google Search Console URL inspection
- Live web search visibility checks
- Local HTML, schema and answerability checks
- Existing external-tag guard

## Search Console Result

The page is indexed and eligible:
- Coverage: Submitted and indexed
- Google canonical: https://vedica-ayurveda.co.il/levinsky-market-food-tour.html
- User canonical: https://vedica-ayurveda.co.il/levinsky-market-food-tour.html
- Crawled as: Mobile
- Page fetch: Successful
- Robots: Allowed
- Sitemap: https://vedica-ayurveda.co.il/sitemap.xml
- Last crawl: 2026-05-27T17:23:47Z

Search Console 28-day performance, 2026-05-19 to 2026-06-15:
- Clicks: 1
- Impressions: 24
- CTR: 4.2%
- Average position: 4.83

Week comparison:
- 2026-06-09 to 2026-06-15: 0 clicks, 15 impressions, avg position 4.93
- 2026-06-02 to 2026-06-08: 0 clicks, 3 impressions, avg position 6.33

The broader page-level query API returned no rows when filtered directly to this page, likely because the page has low query volume in the selected period.

## Live Search Visibility

The page appears for exact/entity-rich checks such as:
- `site:vedica-ayurveda.co.il/levinsky-market-food-tour.html`
- `"Levinsky Market Food Tour in English"`
- `"English-speaking Levinsky Market" "VEDICA"`
- `"Ayurveda" "Levinsky Market" "food tour"`

Broad generic terms such as `Levinsky Market food tour` are competitive. Commonly visible competitors/aggregators include Harry's Baked, Delicious Israel, Tourist Israel, GetYourGuide, Tripadvisor and food/travel blogs.

## On-Page SEO

Passes:
- HTTP status: 200
- Title length: 60 characters
- Meta description length: 153 characters
- Canonical matches live/indexed page
- Robots meta allows indexing
- One H1
- Open Graph and Twitter tags present
- All 6 images have alt text
- 21 internal links
- Sitemap includes the page with hreflang alternates
- Robots.txt allows Googlebot and common AI crawlers

Schema:
- JSON-LD parses without errors
- Types found: Organization, Person, WebSite, WebPage, BreadcrumbList, Service, FAQPage
- FAQ schema contains 11 questions

Repo guard:
- `npm run check:external-tags` passed

## AEO Readiness

Strong answer blocks are present for:
- Is the tour available in English?
- Is this a food tour or a herbal medicine tour?
- Who is the tour for?
- Can it work for native English-speaking groups?
- What details should someone send before booking?
- Can dietary needs be considered?
- What should someone send to request a group quote?

Entity/topic coverage is strong:
- Mentions of Tel Aviv / Levinsky Market: 70
- Mentions of English: 64
- Mentions of Ayurveda, wellness, spices, herbs, infusion or Persian medicine: 138
- WhatsApp CTAs: 6
- Email mentions: 2

## Recommendations

1. Add more external trust signals for this specific tour page: Tripadvisor, Google Business Profile, partner listings or testimonials that mention "Levinsky Market food tour in English".
2. Add visible price/duration guidance if commercially possible. Competitors expose duration and price clearly, which helps both searchers and answer engines.
3. Add a short "quick facts" block near the top with duration, location, language, private/corporate availability, food needs and booking method.
4. Add 2-3 review snippets or client use cases for corporate groups, English-speaking guests and wellness groups.
5. If exact Google Custom Search API testing is required, provide `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`/`cx`, then rerun the CSE query set.

