# SEO/AEO Live Search Check - Clinic Pages

Date: 2026-06-16

Pages:
- https://vedica-ayurveda.co.il/clinic.html
- https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html

## Scope

This mirrors the Levinsky Market report:
- Google Search Console URL inspection
- Google Search Console performance, 2026-05-19 to 2026-06-15
- Live web search visibility checks
- Local HTML, schema and answerability checks
- Existing external-tag guard

Google Custom Search JSON API was not run because no local API key or CSE `cx` ID was found in the repo or environment.

## Search Console Indexing

### Hebrew Clinic Page

URL: https://vedica-ayurveda.co.il/clinic.html

- Coverage: Submitted and indexed
- Google canonical: https://vedica-ayurveda.co.il/clinic.html
- User canonical: https://vedica-ayurveda.co.il/clinic.html
- Crawled as: Mobile
- Page fetch: Successful
- Robots: Allowed
- Last crawl: 2026-05-28T08:34:16Z
- Rich results: Breadcrumbs detected, pass

### English Clinic Page

URL: https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html

- Coverage: Submitted and indexed
- Google canonical: https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html
- User canonical: https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html
- Crawled as: Mobile
- Page fetch: Successful
- Robots: Allowed
- Sitemap: https://vedica-ayurveda.co.il/sitemap.xml
- Last crawl: 2026-05-27T17:20:46Z

## Search Console Performance

Date range: 2026-05-19 to 2026-06-15

| Page | Clicks | Impressions | CTR | Avg position |
|---|---:|---:|---:|---:|
| English clinic | 3 | 50 | 6.0% | 7.70 |
| Hebrew clinic | 0 | 14 | 0.0% | 5.36 |

Week comparison:

| Page | Current clicks | Current impressions | Current pos. | Previous clicks | Previous impressions | Previous pos. |
|---|---:|---:|---:|---:|---:|---:|
| English clinic | 2 | 30 | 5.93 | 1 | 14 | 13.29 |
| Hebrew clinic | 0 | 7 | 5.86 | 0 | 6 | 5.50 |

Notable query/page rows:
- `ayurvedic clinic` -> English clinic: 1 impression, avg position 3
- `ayurvedic pharmacy near me` -> English clinic: 2 impressions, avg position 3
- `ayurveda israel` -> English clinic: 1 impression, avg position 5
- `ayurved hospital near me` -> English clinic: 3 impressions, avg position 7.67
- `אבחון איורוודה` -> Hebrew clinic: 1 impression, avg position 11

## Live Search Visibility

Both clinic pages appear for direct site checks:
- `site:vedica-ayurveda.co.il/clinic.html`
- `site:vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html`

The English page appears for entity-rich English checks such as:
- `English speaking Ayurveda clinic Tel Aviv Inbal Hanasab`
- `Ayurvedic consultation Tel Aviv English VEDICA`

For Hebrew checks, Google often surfaces the home page, Infomed, supporting blog pages and the clinic page together. This is good entity coverage, but it means the Hebrew clinic page is sharing intent with the homepage and Infomed profile.

Common visible competitors/entities:
- VEDA / Roee Raifeld
- Ayurveda Center / Dr. Eran Magon
- PranaVeda
- Infomed expert listings
- Easy profile
- General Ayurvedic consultation directories

## On-Page SEO

### Hebrew Clinic

- HTTP status: 200
- Title length: 48
- Meta description length: 118
- One H1
- 1 image, alt present
- 12 internal links
- 2 external links
- JSON-LD parses without errors
- Schema types: FAQPage, MedicalBusiness, LocalBusiness, HealthAndBeautyBusiness, Service, BreadcrumbList
- FAQ schema questions: 9
- Strong medical caveats: 6 matches for "does not replace" style language

### English Clinic

- HTTP status: 200
- Title length: 60
- Meta description length: 154
- One H1
- 1 image, alt present
- 24 internal links
- 5 external links
- JSON-LD parses without errors
- Schema types: MedicalBusiness, LocalBusiness, HealthAndBeautyBusiness, Service, FAQPage
- FAQ schema questions: 8
- Strong medical caveats: 15 matches for "does not replace" / complementary-care language

Repo guard:
- `npm run check:external-tags` passed

## AEO Readiness

The English clinic page is the stronger AEO page because it gives crisp answers to:
- Are consultations available in English?
- What happens in the first Ayurvedic consultation?
- Can Ayurveda support digestion, stress, sleep or fertility?
- Who is the English-speaking clinic a good fit for?
- What should I prepare before the first consultation?
- Is the clinic suitable for English-speaking patients in Tel Aviv?
- What kind of clinic is VEDICA?
- Does the clinic provide Ayurvedic herbal pills?

The Hebrew clinic page is also strong, especially for:
- What is Ayurveda?
- Digestive support
- Stress and sleep
- Fertility / IVF complementary support
- Who the clinic is for
- What to prepare before the first meeting
- Dosha diagnosis

## Recommendations

1. The English clinic page should remain a priority page. It is already earning 3 clicks and 50 impressions in 28 days, with week-over-week average position improving from 13.29 to 5.93.
2. Add a short, visible "quick facts" block to the English page if not already prominent enough in the rendered layout: address, first-session length, languages, appointment method, complementary-care caveat.
3. Strengthen Hebrew clinic query capture by adding or refining direct phrasing around `אבחון איורוודה`, `קליניקת איורוודה בתל אביב`, and `טיפול איורוודי בתל אביב` without making medical claims.
4. Build more internal links from Hebrew blog posts to `clinic.html` using exact but natural anchors such as `אבחון איורוודה בתל אביב` and `קליניקת איורוודה בתל אביב`.
5. Keep external trust signals active: Infomed, Easy, Nizat and any Google Business Profile/review surface should consistently mention VEDICA, Inbal Hanasab, Tel Aviv, Ayurveda and Persian medicine.

