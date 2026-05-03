# Website Bot Capability Expansion Spec
## Focus Skill: `image-text-optimizer`

## 1. Purpose
Design a dedicated skill that improves website image assets and image-related text so pages become clearer, faster, more accessible, and more discoverable by both search engines and LLM crawlers.

## 2. Problem Statement
Website builders often ship pages with one or more of the following:
- Heavy images that hurt performance.
- Generic or missing alt text.
- Overlong hero copy that reduces clarity.
- Weak text-image alignment (headline says one thing, hero image communicates another).
- Inconsistent metadata and structured content around media.

A focused skill should solve these reliably with low manual effort.

## 3. Scope
In scope:
- Image inventory and audit across HTML pages.
- Alt text generation and normalization.
- Hero section text tightening (headline, subtitle, CTA support line).
- Image compression and format recommendations (without visual degradation).
- Basic accessibility guardrails for image + text combinations.
- LLM discoverability signals related to media content.

Out of scope:
- Full brand redesign.
- Complex retouching (Photoshop-level edits).
- Video/audio editing pipelines.

## 4. Skill Trigger Conditions
Use this skill when requests include topics such as:
- "Fix images", "optimize image performance", "improve alt text", "make hero less text-heavy".
- "Improve accessibility for media", "image SEO", "image + copy alignment".
- "Make the page easier for AI crawlers to understand".

## 5. Inputs
Required inputs:
- Project path.
- HTML/CSS files.
- Image asset folder(s).

Optional inputs:
- Brand voice (tone, style, forbidden phrases).
- Language priority (Hebrew/English/bilingual).
- Hero message priority (conversion goal).

## 6. Outputs
Required outputs:
- Updated HTML with improved `alt` text and tighter on-image copy.
- A short image optimization report per page.
- Change log with before/after snippets.

Optional outputs:
- Suggested image replacements if current assets are semantically weak.
- Reusable text templates for hero/feature cards.

## 7. Workflow
1. Discover pages and image references.
2. Classify images by role: hero, feature, decorative, logo, gallery, social proof.
3. Detect missing or weak alt text.
4. Detect high-risk text density zones (especially hero overlays).
5. Propose concise replacement copy with the same intent.
6. Apply edits with conservative defaults.
7. Run accessibility + SEO checks.
8. Produce verification checklist and report.

## 8. Quality Rules
- Keep hero headline under 10 words (default target).
- Keep hero subtitle under 18 words (default target).
- Avoid repeating the same phrase in both headline and subtitle.
- Alt text must describe purpose, not just object list.
- Decorative images should use empty alt (`alt=""`) where appropriate.
- Do not invent testimonials or factual claims.
- Preserve meaning when shortening copy.

## 9. LLM and SEO Requirements
- Ensure each page has canonical + description.
- Ensure `llms.txt` discoverability path is linked where relevant.
- Keep media-related copy factual and entity-clear.
- Maintain schema consistency when image context changes.

## 10. Acceptance Criteria
The skill is successful when:
- Every meaningful image has quality alt text.
- Hero section is visibly less dense while preserving message.
- No broken image links after edits.
- Accessibility score does not regress.
- SEO score does not regress.
- Manual reviewer can approve copy in under 5 minutes per page.

## 11. Self-Test Plan (Can Be Run Manually)

### A. Fast Structural Checks
1. Run `rg -n "<img" *.html` and confirm all key images have sensible `alt`.
2. Run `rg -n "llms.txt" *.html` and confirm discoverability links are present where expected.
3. Run `rg -n "<h1|hero|whatsapp|contact" index.html` and verify hero text is concise.

Pass condition:
- No critical image without purposeful alt text.
- No accidental hero text expansion.

### B. Link and Load Checks
1. Start local server: `python3 -m http.server 4173`.
2. Open key pages (`/`, `/contact.html`, `/blog.html`) and verify images load.
3. Check there are no 404s in Network panel for media assets.

Pass condition:
- All key images load successfully.

### C. Lighthouse Spot Checks
1. Run Lighthouse for `index.html` and `contact.html`.
2. Compare Accessibility and SEO with previous baseline.

Pass condition:
- Accessibility: no regression.
- SEO: no regression.

### D. Human Copy Review
1. Read hero section on mobile width.
2. Ask: "Can I understand offer + action in 5 seconds?"
3. Ask: "Is there any sentence that can be removed with no loss?"

Pass condition:
- Reviewer answers "yes" to clarity and "no" to redundancy.

### E. Alt Text Quality Review
For 5 random images:
1. Read alt text out loud.
2. Ask: "Would this help a screen-reader user understand why the image is here?"

Pass condition:
- At least 4/5 are clearly purpose-oriented.

## 12. Suggested Skill Folder Layout
image-text-optimizer/
- SKILL.md
- agents/openai.yaml
- scripts/
- references/
- assets/

## 13. Suggested First Scripts
- `scripts/audit_images.sh`: inventory images and alt status.
- `scripts/check_hero_density.sh`: detect long hero copy.
- `scripts/report_media_quality.py`: produce per-page report.

## 14. Risks and Mitigations
- Risk: Over-shortening copy and losing meaning.
  Mitigation: Keep intent lock rule and explicit reviewer step.
- Risk: Generic alt text.
  Mitigation: role-based alt templates by image type.
- Risk: Over-editing design system styles.
  Mitigation: change copy and attributes first; style changes only when measurable issue exists.

## 15. Rollout Strategy
- Phase 1: Home + Contact.
- Phase 2: Core service pages.
- Phase 3: Blog templates + archive pages.
- Phase 4: Full media audit and periodic recheck.

## 16. General Lessons Learned (From This Project)

### A. Conversion Lessons
- Hero sections become weaker when text grows beyond a quick 5-second read.
- A tighter headline + one clear CTA usually outperforms long explanatory hero text.
- Trust can be built via process clarity (who, how, where) even before testimonials exist.
- Never use fabricated testimonials; use process proof until real reviews are collected.

### B. Accessibility Lessons
- Accessibility regressions often come from small UI details, not large layout issues.
- Color contrast and heading hierarchy are frequent failure points and should be checked early.
- Social icon links should have visible text/accessibility-aligned naming to avoid label mismatches.
- Form fields need explicit label associations (`for` + `id`) to pass reliably.

### C. SEO Lessons
- Missing `meta description` tags often remain hidden in older pages and blog posts.
- Canonical consistency is easy to maintain once audited, but hard to recover after drift.
- One meaningful `h1` per page keeps content hierarchy cleaner and easier to parse.

### D. Analytics Lessons
- Mixed GA/GTM setups across pages destroy measurement consistency.
- Track core events first: WhatsApp click, form attempt, form success, form error.
- A website cannot be optimized for conversion if events are not trustworthy.

### E. LLM Discoverability Lessons
- `llms.txt` is useful only when coverage is complete and links are maintained.
- If LLM discoverability is a goal, treat it like sitemap hygiene: audit regularly.
- Entity clarity in copy helps both search engines and language-model crawlers.

### F. Execution Lessons
- Batch fixes are efficient, but each batch still needs a verification loop.
- Lightweight automated checks + manual copy review is the best reliability mix.
- Prioritize no-regression rules (accessibility, SEO, broken links) on every iteration.

## 17. Advanced Lessons (Governance and Scale)

### A. Skill Lifecycle and Release Governance
- Use semantic versioning for skills (`MAJOR.MINOR.PATCH`) and track changes by capability.
- Define release gates: pass lint, pass Lighthouse thresholds, pass manual copy QA.
- Keep rollback-ready commits so content regressions can be reverted quickly.

### B. Multilingual Content Operations
- Maintain source-of-truth copy in one language and structured translation rules for others.
- Enforce terminology consistency (medical terms, service names, CTA verbs).
- Validate each language independently for accessibility and readability.

### C. Content Policy and Claims Control
- Define allowed claim types (descriptive/process-based) vs. restricted claim types (outcome promises).
- Require evidence or disclaimers for sensitive health-related statements.
- Keep testimonial policy explicit: only verified real testimonials with publishing consent.

### D. KPI and Monitoring Framework
- Track north-star KPI: qualified lead submissions.
- Track support KPIs: WhatsApp click-through, form completion rate, page-level drop-off.
- Add post-release checkpoints (24h/7d/30d) to confirm improvements hold in real traffic.
