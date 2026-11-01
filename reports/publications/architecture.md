# Publications architecture and phase record

## Phase 0: discovery and baseline

The existing website is buildless HTML/CSS/JavaScript under `docs/`. It has no
website `package.json`, framework, router, database, or automated test runner.
`docs/assets/app.js` fetches the original Markdown guide, parses its H1 chapters,
and routes with URL fragments. The current source is
`content/guides/end-to-end-fde-learning-map/README.md`.

Learning completion uses `fde-field-guide-progress-v1` in localStorage. Theme
uses `fde-field-guide-theme`. Completion is explicit and persisted on click.
These keys and chapter slugs must remain unchanged. Publications will have a
separate progress namespace.

The existing design tokens in `docs/assets/styles.css`, Manrope / DM Mono fonts,
dark navy surfaces, green accent, sidebar, theme toggle, and mobile menu are
reusable. The existing FDE renderer remains isolated from the article renderer.

Baseline commands: `git diff --check`, `node --check docs/assets/app.js`, and an
isolated headless Chromium functional check using the already installed
Playwright runtime. Actual results are recorded in [baseline.json](baseline.json).
The baseline checked chapter navigation, 27 trackable chapters, search and empty
results, persistence across reload, mobile menu, and overflow at 1440 / 390 px.
No website build command existed. Existing repository reorganization edits were
already present in Git and are not reverted or committed by this task.

The interactive browser connector was unavailable. Automated Chromium tests use
an isolated context and do not read or modify the user's existing browser data.

## Phase 1: minimal extension and routes

Keep the FDE reader at the existing site root and all existing fragment routes.
Add real static pages under `publications/`, with no frontend framework or
database. A Python build discovers Markdown, validates metadata, renders safe
HTML, and emits an immutable static artifact. Browser JavaScript adds search,
filters, current section highlighting, and explicit reading completion.

| Relative route | Responsibility |
| --- | --- |
| `/` and `/#<existing-chapter>` | Original FDE curriculum |
| `/publications/` | Publications overview and searchable index |
| `/publications/latest/` | Chronological publication listing |
| `/publications/topics/` | Taxonomy and public article counts |
| `/publications/topics/<slug>/` | Articles in a configured topic |
| `/publications/series/` and `/publications/series/<slug>/` | Explicit ordered collections |
| `/publications/paths/` and `/publications/paths/<slug>/` | Learning paths across topics |
| `/publications/<slug>/` | Dedicated article page |

Reserved index slugs are rejected for articles. All routes are relative to the
configured deployment base, so GitHub Pages project subpaths work. FDE's
publication card links directly to its existing curriculum route; a publication
detail entry points readers to that same canonical experience.

Keep the existing `content/articles/` and `content/guides/` sources. New Markdown
uses frontmatter; a metadata sidecar registers FDE without changing its bytes.
Taxonomy, series, learning paths, and site settings are data files. Templates and
drafts are not copied to the public artifact.

## Risks and policies

- A static file server at the repository root exposes source files. Public
  previews and deployment must serve only the generated site artifact.
- Scheduled content is included only when its timestamp is reached at build
  time. No unattended publication is promised without an authorized scheduler.
- GitHub Pages currently deploys the `docs/` directory. The workflow must build
  and upload only the generated artifact, after running validation and tests.
- The canonical base is explicit site configuration, not inferred from browser
  origins or import timestamps. The configured production URL is a deployment
  target; this task does not verify or deploy the live website.
- Archived publications retain their URLs with an archive notice, and are
  excluded from discovery, search, feed, and sitemap.
- Rendering accepts Markdown and safe technical markup. Embedded scripts and
  active HTML are removed. MDX execution is unnecessary for the current stack.
