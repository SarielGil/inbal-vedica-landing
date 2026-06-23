# SEO/AEO Weekly Retest

Date: 2026-06-23
Site: https://vedica-ayurveda.co.il/

## Scope

Retest of the priority SEO/AEO pages after the 2026-06-16 service-first copy updates:

- https://vedica-ayurveda.co.il/
- https://vedica-ayurveda.co.il/clinic.html
- https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html
- https://vedica-ayurveda.co.il/levinsky-market-food-tour.html

Google Custom Search JSON API was not run because this environment still has no `GOOGLE_CSE_ID` / `cx` available. The test used Google Search Console, live web search, local HTML/schema checks, live deployed HTML checks, sitemap validation and the repo external-tag guard.

## Validation

- Search Console snapshot saved to `seo-logs/search-console/2026-06-23/summary.md`
- `xmllint --noout sitemap.xml`: passed
- Live sitemap: HTTP 200
- `npm run check:external-tags`: passed
- Local JSON-LD parsing: passed on all four pages
- Live deployed HTML contains the updated service-first meta descriptions

## Search Console Indexing

All four tested pages are submitted and indexed with correct Google-selected canonicals.

| Page | Coverage | Last crawl | Canonical |
|---|---|---:|---|
| Home | Submitted and indexed | 2026-06-19T14:09:39Z | https://vedica-ayurveda.co.il/ |
| Hebrew clinic | Submitted and indexed | 2026-06-11T07:00:28Z | https://vedica-ayurveda.co.il/clinic.html |
| English clinic | Submitted and indexed | 2026-05-27T17:20:46Z | https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html |
| Levinsky tour | Submitted and indexed | 2026-05-27T17:23:47Z | https://vedica-ayurveda.co.il/levinsky-market-food-tour.html |

Important: Google has recrawled the home page after the 2026-06-16 updates, but has not yet recrawled the English clinic or Levinsky tour pages according to URL Inspection.

## 28-Day Performance

Range: 2026-05-26 to 2026-06-22.

| Page | Clicks | Previous test | Impressions | Previous test | Avg position | Previous test |
|---|---:|---:|---:|---:|---:|---:|
| Home | 20 | 27 | 269 | 190 | 6.36 | 5.31 |
| Hebrew clinic | 0 | 0 | 26 | 14 | 5.85 | 5.36 |
| English clinic | 3 | 3 | 91 | 50 | 6.62 | 7.70 |
| Levinsky tour | 1 | 1 | 50 | 24 | 5.74 | 4.83 |

Interpretation:

- Impressions are up on all four priority pages.
- English clinic is the strongest improvement: impressions rose from 50 to 91 and average position improved from 7.70 to 6.62.
- Levinsky tour impressions more than doubled, from 24 to 50, but average position softened from 4.83 to 5.74.
- Home page impressions rose, but clicks and CTR declined in the rolling 28-day window.

## 7-Day Comparison

Current: 2026-06-16 to 2026-06-22.
Previous: 2026-06-09 to 2026-06-15.

| Page | Current clicks | Previous clicks | Current impressions | Previous impressions | Current pos. | Previous pos. |
|---|---:|---:|---:|---:|---:|---:|
| Home | 4 | 4 | 92 | 80 | 6.73 | 7.20 |
| Hebrew clinic | 0 | 0 | 11 | 8 | 4.91 | 8.00 |
| English clinic | 0 | 2 | 40 | 31 | 5.25 | 5.97 |
| Levinsky tour | 0 | 0 | 24 | 17 | 6.50 | 5.24 |

Interpretation:

- Home page: impressions up and position improved week-over-week; clicks flat.
- Hebrew clinic: small but meaningful visibility improvement; average position improved from 8.00 to 4.91.
- English clinic: impressions and position improved, but clicks dropped from 2 to 0 this week.
- Levinsky tour: impressions up, position softer; still early and low-volume.

## Query Signals

Notable query/page rows:

- `רפואה איורוודית` -> home: 1 click, 10 impressions, avg position 8.80
- `מטפלת איורוודה` -> home: 1 impression, avg position 7
- `אבחון איורוודה` -> clinic: 1 impression, avg position 11
- `ayurvedic consultation` -> English clinic: 1 impression, avg position 2
- `ayurvedic clinic` -> English clinic: 1 impression, avg position 3
- `ayurvedic pharmacy near me` -> English clinic: 2 impressions, avg position 3
- `levinsky market food tour` -> Levinsky tour: 1 impression, avg position 19

## Live Search Visibility

Representative live web search showed VEDICA pages appearing for:

- English clinic/service queries
- Levinsky Market food tour with VEDICA/entity terms
- VEDICA Ayurveda Tel Aviv/entity searches
- Hebrew clinic/Ayurveda queries

Observed competitors/directories in the same result sets include VEDA, Ayurveda Center, PranaVeda, Infomed, Easy, Harry's Baked, Delicious Israel, Tripadvisor, Abraham Tours and Tourist Israel.

Snippet note:

- Live deployed HTML has the new service-first copy.
- Some Google/search snippets still display older name-heavy text for the home and English clinic pages. Treat this as snippet/index lag until Google recrawls those pages again and Search Console confirms newer crawl dates.

## On-Page SEO/AEO

All four pages remain structurally sound:

- One H1 per page
- Title and meta description lengths are sane
- Canonicals match intended URLs
- Robots meta allows indexing
- Image alt coverage is complete
- JSON-LD parses without errors
- FAQ/service/local-business schema remains present
- Specific-name usage is now low in discovery surfaces and preserved mainly in schema/review/trust contexts

## Recommendations

1. Wait for recrawl of `english-speaking-ayurveda-clinic-tel-aviv.html` and `levinsky-market-food-tour.html`; URL Inspection still shows May 27 crawls.
2. If you want faster refresh, submit the sitemap in Search Console and manually request indexing for the English clinic and Levinsky tour pages in the Search Console UI.
3. Keep the service-first copy. It is increasing impressions, especially for English clinic and Levinsky tour.
4. Improve CTR next: add clearer visible quick facts for English clinic and Levinsky tour, especially duration, location, what is included and booking method.
5. Build internal links to Hebrew clinic with anchors around `אבחון איורוודה`, `קליניקת איורוודה בתל אביב`, and `טיפול איורוודי בתל אביב`.
6. Retest again after the English clinic and Levinsky tour pages show a fresh crawl date, or in another 7-10 days if no recrawl happens.

