# Portfolio v2.0 audit and implementation plan

## Baseline reviewed

The live GitHub Pages site returned HTTP 200 at 1440 px and 390 px. Both views fit their viewport. Baseline capture is in output/playwright/v1-1440.png and v1-390.png. The remote main and original checkout were both at 1ba1baf. Work is isolated on the local portfolio/v2.0 branch in a separate worktree.

| Area | Existing site | v2.0 decision |
| --- | --- | --- |
| Navigation | Seven links and repeated header markup. Homepage order changes in JavaScript by width. | Projects, Method, About and Contact. Use one reading order. Retain old page URLs and homepage anchors. |
| Identity | Strong SCIENCE × APPLICATION mark. Opening copy concentrates on materials computation. | Keep the mark, dark blue and mint. Position Guanyu as a researcher and technology builder, grounded in materials science. |
| Project depth | Three doctoral project pages, one tools overview and an AI-for-science direction. External work is mostly grouped under tools. | Keep the existing research body copy and disclosure. Give six public projects direct access and evidence-led case studies. Keep exploratory work visibly distinct. |
| Mobile | Current hero, small technical labels and collapsible navigation fit 390 px. Selected projects move ahead of the skills section. | Larger body and control text. The featured work starts immediately after the hero. Evidence links and gallery filters remain usable by keyboard and touch. |
| Search and sharing | Canonicals and common Open Graph imagery exist. | Generate page-specific titles, descriptions and canonicals, a sitemap and a refreshed public-safe social card. |
| Privacy | Doctoral results are restricted. Public pages show general methods, approved contact links and conceptual diagrams. | Preserve this boundary verbatim. Copy public project artifacts only where there is a clear source and permission. Keep career samples synthetic and avoid private research paths, results or account records. |

## Information architecture and content strategy

- The introduction identifies the person, their technical foundation and the kind of work they deliver. An actual verification artifact gives a technical reader an immediate entry point.
- Three featured projects represent numerical verification, local decision-support software and a usable visualisation tool. Each links to a case study. The full catalogue is grouped into Research & Engineering, AI & Knowledge Engineering and Innovation Lab, with a category filter and no-script support.
- Each new case study explains the decision that shaped that project, the implementation, evidence and scope. Evidence lives alongside the relevant claim. Two writing projects cross-link as method extraction and method application.
- The method section draws on named project decisions rather than describing abstract principles. About carries the user-provided viva result, correction status and broader career interests. The contact block keeps the three previously approved channels.
- English is the initial locale. Keep source content and labels separate from rendering. A later locale can supply translated content and a locale-specific path without changing the project identifiers.

## Implementation sequence

1. Audit live layout and public metadata. Inspect pinned project source, versioned reports and evidence artifacts. Record claims and limits in the evidence inventory.
2. Generate a static homepage and six case study pages from shared project metadata. Stamp the common navigation into legacy pages while preserving research body copy and earlier assets.
3. Integrate checked public evidence assets and maintain a provenance list.
4. Run build and disclosure checks, then verify rendered desktop/mobile pages, navigation, filters, links and accessibility. Capture screenshots and preserve the results.
5. Record changes and maintenance instructions. Submit a local branch and preview for review before formal merge or deployment.
