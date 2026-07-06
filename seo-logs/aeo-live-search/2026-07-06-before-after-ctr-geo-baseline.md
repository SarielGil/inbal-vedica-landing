# SEO/AEO/GEO Baseline - 2026-07-06

## Verdict

Mixed but improving before the metadata/GEO owner changes are deployed.

- Visibility improved: 28-day impressions rose from 1,565 in the 2026-07-05 snapshot to 1,699 in the 2026-07-06 snapshot.
- Clicks improved slightly: 33 to 36.
- CTR is nearly flat: 2.11% to 2.12%.
- Average position improved: 6.64 to 6.43.
- This is a pre-deploy/pre-recrawl baseline. Live Google snippets still show the old title patterns without Inbal's name in the main Vedica title links.

## Search Console

- Snapshot date: 2026-07-06
- Lookback period: 2026-06-08 to 2026-07-05
- Current comparison period: 2026-06-29 to 2026-07-05
- Previous comparison period: 2026-06-22 to 2026-06-28

### 28-Day Baseline

| Snapshot | Lookback | Clicks | Impressions | CTR | Avg position |
|---|---|---:|---:|---:|---:|
| 2026-07-02 | 2026-06-04 to 2026-07-01 | 34 | 1,232 | 2.76% | 7.50 |
| 2026-07-05 | 2026-06-07 to 2026-07-04 | 33 | 1,565 | 2.11% | 6.64 |
| 2026-07-06 | 2026-06-08 to 2026-07-05 | 36 | 1,699 | 2.12% | 6.43 |

### Week-Over-Week

| Period | Clicks | Impressions | CTR | Avg position |
|---|---:|---:|---:|---:|
| 2026-06-22 to 2026-06-28 | 7 | 479 | 1.46% | 6.61 |
| 2026-06-29 to 2026-07-05 | 10 | 639 | 1.56% | 5.24 |

Interpretation: the site is being shown more often and in better positions, but CTR is still low. This is the right moment to test a stronger trust cue in titles/descriptions.

### Changed-Page Baseline

| Page | Current clicks | Current impressions | CTR | Avg position | Note |
|---|---:|---:|---:|---:|---|
| Home | 7 | 320 | 2.19% | 4.45 | Main CTR test page: added `ענבל הנסב` to title/meta/social. |
| Hebrew clinic | 0 | 36 | 0.00% | 6.03 | Strong zero-click opportunity. Added name to title/meta/social and `owner` schema. |
| English clinic | 1 | 73 | 1.37% | 4.96 | Added `Inbal Hanasab` to title/meta/social and `owner` schema. |
| About | 0 | 18 | 0.00% | 4.33 | Already name-led; useful control for brand/person trust. |

## Indexing

- Indexed: home, clinic, English clinic, Levinsky tour, stress/sleep blog, Persian medicine.
- Not indexed: `ayurveda-fertility-ivf-tel-aviv.html` is still discovered but not indexed.
- Unknown to Google: `ayurveda-sensitive-digestion-fatigue-tel-aviv.html`.
- `llms.txt`, `sitemap.xml`, and `robots.txt` showed as unknown in URL Inspection, which is normal for non-ranking utility files but useful to track after adding `llms.txt` to the sitemap.

## SEO/AEO/GEO

- Sitemap updated locally on 2026-07-06:
  - `/`
  - `/clinic.html`
  - `/english-speaking-ayurveda-clinic-tel-aviv.html`
  - `/llms.txt` added to sitemap.
- `llms.txt` now states that Inbal Hanasab is founder and owner of VEDICA.
- AEO answer blocks in `llms.txt` now connect VEDICA to Inbal as owner for Hebrew and English clinic queries.
- JSON-LD now includes `owner` in addition to `founder` for home, Hebrew clinic and English clinic.
- Google Custom Search API was not used because `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`, and `cx` were not available in the shell environment.
- OpenFound was not refreshed in this run.

## Technical Checks

- `xmllint --noout sitemap.xml`: pass.
- `npm run check:external-tags`: pass.
- `git diff --check`: pass.
- JSON-LD validation: 32 valid blocks across root HTML files.
- Live HTTP checks: priority URLs, `llms.txt`, `sitemap.xml`, and `robots.txt` all returned HTTP 200.

## Public Search Notes

Public search samples on 2026-07-06 still showed pre-change Vedica snippets:

- Hebrew clinic searches show Vedica with titles such as `קליניקת איורוודה בתל אביב | אבחון 2 שעות | 20 חוות דעת`.
- English clinic searches show `English Ayurveda Clinic Tel Aviv | 20 Reviews | VEDICA`.
- Competitors continue to use practitioner-name trust cues:
  - PranaVeda / Lital Simon.
  - Ayurveda Center / Dr. Eran Magon.
  - Infomed directory exposes Inbal Hanasab with 20 reviews.

## Fixes Made Before This Baseline

- `index.html`: added Inbal's name to title, meta description and Open Graph text.
- `clinic.html`: added Inbal's name to title, meta description, Open Graph, Twitter metadata and JSON-LD owner.
- `english-speaking-ayurveda-clinic-tel-aviv.html`: added Inbal Hanasab to title, meta description, Open Graph, Twitter metadata and JSON-LD owner.
- `llms.txt`: added founder/owner language and owner-aware AEO answers.
- `sitemap.xml`: bumped changed URLs to 2026-07-06 and added `llms.txt`.

## After-Change Measurement Plan

1. Deploy the changed files.
2. Submit the sitemap after the deployed sitemap contains the 2026-07-06 lastmod values.
3. In Search Console UI, request indexing for:
   - `https://vedica-ayurveda.co.il/`
   - `https://vedica-ayurveda.co.il/clinic.html`
   - `https://vedica-ayurveda.co.il/english-speaking-ayurveda-clinic-tel-aviv.html`
4. Recheck live snippets after Google recrawls. The home page was last crawled on 2026-07-05, clinic on 2026-06-28 and English clinic on 2026-07-02.
5. Compare CTR after at least 7 days of post-recrawl data, preferably in a snapshot dated 2026-07-13 or later.

## Actionable Next

- Do not judge the name/title test until Google recrawls and Search Console has post-recrawl impressions.
- If the name-led clinic snippets improve CTR, consider adding Inbal's name to selected high-intent snippets where trust matters.
- If CTR drops, revert homepage title to clinic-first/review-first and keep Inbal primarily in schema, About and reviews.
