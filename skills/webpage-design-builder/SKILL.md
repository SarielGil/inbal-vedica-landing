---
name: webpage-design-builder
description: Design and redesign website pages into modern, useful, conversion-focused layouts with strong visual hierarchy, cleaner hero sections, and mobile-first usability. Use when users ask to modernize design, improve UX, tighten copy density, upgrade navigation, or align multiple pages to one shared design system.
---

# Webpage Design Builder

Apply this skill to ship practical, modern page redesigns without breaking content intent, brand identity, SEO signals, or accessibility.

## Workflow

1. Audit the page quickly before editing.
- Run `scripts/audit_ui.sh` on target pages.
- Run `scripts/check_hero_copy.py` to detect dense hero copy.
- Load [references/design-qa-checklist.md](references/design-qa-checklist.md) for pass/fail checks.

2. Choose redesign depth.
- Use `surface-refresh` for typography, spacing, hierarchy, and CTA clarity only.
- Use `structural-redesign` when navigation, hero layout, and section order need changes.
- Preserve existing design patterns if the site already has a strong design system.

3. Define the page shell first.
- Build consistent navigation, hero, section rhythm, and footer patterns.
- Use shared classes/tokens for repeatable styling across pages.
- Keep visual direction intentional; avoid generic boilerplate aesthetics.

4. Improve content utility.
- Keep offer/value clear in the first viewport.
- Reduce hero text density while preserving meaning.
- Add quick-path links so users can self-route by need.
- Use [references/section-blueprints.md](references/section-blueprints.md) for section structures.

5. Apply accessibility and trust guardrails.
- Preserve heading hierarchy (`h1` once, then logical `h2`/`h3`).
- Maintain or improve color contrast and link clarity.
- Ensure image alt text is purposeful (`alt=""` for decorative images).
- Keep forms clearly labeled and tap targets usable on mobile.

6. Validate after edits.
- Re-run `scripts/audit_ui.sh` and `scripts/check_hero_copy.py`.
- Confirm no broken links/media and no CTA regressions.
- Report exactly what changed and why.

## Design Guardrails

- Build one clear visual direction per page (typography, palette, density, motion).
- Avoid default-looking layouts and interchangeable component soup.
- Keep hero headline concise and outcome-oriented.
- Prefer one primary CTA plus one secondary CTA in top sections.
- Use gradients/textures/shapes subtly; avoid flat white-only backgrounds.
- Use purposeful micro-motion only where it supports hierarchy.

## Copy Density Defaults

- Hero headline target: `<= 10` words.
- Hero subtitle target: `<= 18` words.
- One primary CTA label: `2-5` words.
- Avoid repeating the same phrase in headline and subtitle.

Adjust only when meaning would be lost.

## Deliverables

For each redesign task, provide:
- Updated files.
- A short before/after summary of UX improvements.
- Any residual risks (for example, images that still need replacement assets).
- Verification results from local checks.
