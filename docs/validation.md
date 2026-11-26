# Portfolio v2.0 validation

Review date 26 November 2026. The local candidate uses a separate worktree and branch. The GitHub Pages source remains at baseline 1ba1baf.

## Browser and source checks

| Check | Result |
| --- | --- |
| Real Chromium layout | All 12 HTML pages returned 200 at 320, 390, 768, 1024 and 1440 px, for 60 checks. No horizontal overflow, failed image decode, missing or duplicate H1, or uncaught page error. |
| Visual review | Desktop and mobile homepage, an engineering report page and a synthetic application screenshot were inspected visually. The plot fits the hero and case layout. Dense scientific images link to full-size evidence. |
| Navigation and filters | Keyboard skip link, mobile menu open and dismissal, restored focus after Escape, anchor navigation and a case route passed. The Research, Knowledge and Innovation filters showed 5, 3 and 3 items. The full directory showed 11. |
| Scripts disabled | All 11 project links, four main navigation links and three contact links stayed visible at 390 px. |
| Accessibility | Axe 4.10.3 WCAG 2.0 and 2.1 A/AA checks found no automated violations across 12 pages at 390 and 1440 px. Keyboard checks were separate. Axe deferred text over gradients and some separator glyphs. Checked the gradient text against its lightest background stop (minimum 7.85:1). No screen-reader testing was performed. |
| SEO and sharing | Unique document titles and canonical routes, per-page descriptions, Open Graph and Twitter metadata, matching 12-page sitemap and 1200 × 630 social image verified locally. Platform-specific live share rendering is pending public deployment. |
| Internal links | Repo verifier checked 247 internal references and applicable anchor targets. |
| External links | 42 of 43 public HTTPS destinations returned 200 by unauthenticated GET, including both live demos and all on-site pinned evidence links. LinkedIn returned 999 after redirecting to the same profile path. The profile’s visibility to a LinkedIn user remains unverified. The approved mailto link was inspected without sending mail. |
| Evidence alignment | Each case has a pinned primary-source record. 39 distinct blob links in the evidence document were additionally matched against their public commit trees. |
| Disclosure | The legacy detail-page main bodies match baseline 1ba1baf. The approved disclosure remains on the homepage and research pages. The publishable file and media lists exclude QA output, local paths, raw research data and old private assets. Screenshots from separate projects use public or synthetic inputs only. |

The external project checks were scoped to the cited versions and relevant artifacts. The review reran 14 synthetic Career Intelligence tests and 66 investment preview, simulation and walk-forward tests, all passing. The Distill scaffold/validator smoke test exercised workspace creation, invalid records and overwrite protection. Palette’s public CI and both local-in-browser synthetic demo modes were reviewed. OpenFOAM results were checked against the archived report and data rather than recomputed.

## Four visitor walkthroughs

| Viewpoint | Route and conclusion |
| --- | --- |
| Scientific or engineering hiring manager | Home → OpenFOAM → verification report → Research & Engineering. The route shows simulation setup awareness, a failed conservation check, scoped numerical evidence and links to existing doctoral methods. |
| AI and technology hiring manager | Catalogue → Writing Method → companion Editor → rule catalogue. The two cases show structured knowledge extraction and application, with human review retained. The case studies make no comparative model-quality claim. |
| Industry collaborator | OpenFOAM or Career Intelligence → evidence and scope → Contact. The route distinguishes numerical checks from experimental evidence, and a single-user workflow from a deployable multi-user service. |
| General technical visitor | Featured Palette Miner or Career Intelligence → public demo → source. The project states and synthetic examples indicate what someone can try today. |

These are internal walkthroughs, with no recruitment, hiring or adoption outcomes implied.

## Local review evidence

- `output/playwright/home-1440.png` and `home-390.png` contain full-page desktop and mobile home captures.
- The same directory contains both sizes for OpenFOAM, Career Intelligence, Palette Miner, Investment Research and both writing skills, plus two screenshots of the public baseline.
- `output/browser-check.json` records browser metrics and automated checks. `output/external-links.json` records HTTP status and redirects.
- `docs/project-evidence.md` maps technical statements and project limits to source records.

## Confirm before merging

- Confirm the public wording of the viva date, minor corrections and current correction status. The current text reflects the brief and carries no award claim.
- Confirm the public positioning “Researcher & technology builder” and the level of first-person ownership in the method and About copy.
- Confirm the preferred description of your individual OpenFOAM, Career Intelligence, writing-skill and Palette contributions if you want more detail. The portfolio uses project-level wording where the public record does not distinguish human and AI work.
- Confirm you want Portfolio v2.0 merged and published at the existing GitHub Pages URL.
