# Portfolio v2.0

Guanyu Zou’s research and technology portfolio. The site is static HTML, CSS and JavaScript. It runs on GitHub Pages without a server build.

## Preview and build

Run these commands from the checkout root using Python 3.10 or newer.

```text
python scripts/build.py
python scripts/verify.py
python -m http.server 8769 --bind 127.0.0.1
```

Open <http://127.0.0.1:8769/>. The server is accessible on the machine running it. Stop it with Ctrl+C. The preview uses the production canonical URLs for SEO verification. A local preview does not alter GitHub Pages.

## Maintain projects

1. Edit `content/projects.en.json`. Each entry has a stable ID, title, category, summary, status, outcome and technology list. New case studies also include the snapshot date, source revision, repository, sections and evidence links. Add a demo only if it is usable and its data is suitable for public viewing.
2. For each result or technical claim, record the corresponding report, test or implementation at a pinned revision. Use the claim and evidence map for the longer explanation. Keep a project’s limitations near its results.
3. Store approved project images under `assets/projects/`. Provide an accessible description, caption, provenance and rights. A software licence alone may not cover third-party images or data. Include the applicable notices when redistributing art or captures.
4. Choose featured project IDs in the catalogue. Desktop, mobile and scripts-disabled visitors see the same project inventory. The featured list is editorial and separate from the category filter.
5. Run the build, verify the changed output and review the resulting HTML. Commit source and generated pages together. The original doctoral pages remain standalone. Their research text is preserved, with shared navigation stamped in during generation.

Use `content/home.en.html` for home copy, `content/layout.html` for the document shell, and `portfolio-v2.css` for the shared v2 appearance. Change approved contact links through `site-config.js`. The project IDs and evidence paths are language independent. A future Chinese edition can add localized content and strings under its own route, while retaining stable project IDs. A bilingual UI is outside this release.

## Review before publication

Read the [audit and plan](docs/portfolio-audit.md), [evidence map](docs/project-evidence.md), [media notices](docs/media-notices.md), [validation report](docs/validation.md) and [changelog](CHANGELOG.md). Confirm any new public claims or assets. Changes to the local review branch do not deploy. When approved, merge the reviewed branch into the existing Pages source branch and verify the deployed URLs and social image.

`output/` is ignored and kept for local screenshots and QA logs. The previous public site remains available at its original revision and URL during review.
