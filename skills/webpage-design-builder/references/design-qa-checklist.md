# Design QA Checklist

Use this checklist after any page redesign.

## Structure

- Exactly one `h1` on the page.
- Hero communicates: who it is for, what value is offered, what to do next.
- Sections appear in useful order: value -> trust/process -> details -> CTA.
- Navigation works on mobile and desktop.

## Visual Clarity

- Typography scale feels intentional, not flat.
- Spacing rhythm is consistent between sections.
- Primary action is visually dominant.
- Cards and containers use consistent corner radius/shadow language.

## Usability

- Primary CTA appears above the fold on mobile.
- Tap targets are comfortably clickable.
- Key links are discoverable without hunting.
- Forms are easy to scan and complete.

## Accessibility

- Contrast remains readable for body text and buttons.
- Every meaningful image has purposeful `alt` text.
- Decorative images use empty alt (`alt=""`).
- Inputs have visible labels bound by `for` + `id`.

## SEO / Entity Clarity

- `meta description` exists and matches page intent.
- Canonical URL exists.
- Main page intent is obvious from `h1` + intro text.
- Contact/location details are easy to find when relevant.
- New landing pages are linked from at least one high-authority internal page, not only listed in sitemap/hreflang.
- Multilingual alternate pages have reciprocal `hreflang`, matching canonical URLs, and sitemap alternates.
- Sitemap `lastmod` reflects newly changed or newly published priority pages.
- For fresh pages, distinguish crawlability from indexing: verify `200 OK`, `index, follow`, canonical, robots, sitemap, and internal links before judging SERP absence as ranking degradation.
- Page titles preserve proven exact-match/high-intent terms unless there is a deliberate keyword strategy change.

## Regression Checks

- No broken local links.
- No broken image references.
- No accidental removal of analytics snippets.
- No content claim inflation during copy tightening.
- Search/SEO changes include a before/after note for titles, H1s, internal links, sitemap dates, and indexing expectations.
