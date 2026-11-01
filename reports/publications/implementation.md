# Technical Publications implementation report

## Result

The existing FDE website has been extended with a content-driven Technical
Publications library. It runs locally at <http://localhost:8000/publications/>.
The original reader remains available at
<http://localhost:8000/docs/#end-to-end-fde-learning-map> and the deployed site root.

One real publication is registered: the original FDE Field Guide. Test articles
exist only in temporary/generated fixtures and never enter the public artifact.

## Architecture

- Existing stack: static HTML, CSS, browser JavaScript, fragment-based FDE
  routing, localStorage chapter completion, and GitHub Pages deployment.
- Extension: Python build-time metadata discovery, validation, Markdown
  rendering, and real static routes under `publications/`.
- Content stays in `content/articles/` and `content/guides/`. The FDE source uses
  a metadata sidecar so its instructional bytes remain unchanged.
- Taxonomy, publication types, series, paths, and canonical URL locks are data
  files. New publications do not require frontend edits.
- The local server serves only `build/site/`, retains `/docs/` compatibility,
  and rebuilds changed content on the next request.
- No frontend framework, database, external search service, or MDX runtime was
  introduced. Existing design tokens, typography, dark/light themes, and reader
  styling are reused.

Build dependencies have specific roles: PyYAML parses metadata; jsonschema
validates it; Markdown renders prose, tables and footnotes; Pygments highlights
code; latex2mathml renders equations to native MathML; bleach sanitizes HTML.
Playwright is optional test tooling and is not shipped to visitors.

## Phase acceptance record

| Phase | Evidence and outcome |
| --- | --- |
| 0 — Discovery and baseline | [Architecture assessment](architecture.md), [baseline](baseline.json), original browser functional checks |
| 1 — Information architecture | Static route hierarchy documented; existing root and fragment routes retained |
| 2 — Schema and taxonomy | Required metadata, dates, categories, duplicate identities, references, URL locks, and cycles tested |
| 3 — Publishing engine | Automatic source discovery; draft/review/future filtering; archived route retention; atomic builds; separate previews |
| 4 — Homepage | Real featured/latest content, domain counts, collections, search controls, and empty states; desktop/mobile screenshots inspected |
| 5 — Reading experience | Anchors, sticky TOC, code, tables, MathML, safe diagrams, references, related articles, explicit completion |
| 6 — Discovery | Body/title/topic/tag/technology search; combined filters; URL state; deterministic sorting; relevance ranking |
| 7 — Series and paths | Explicit ordered collections, previous/next, cross-topic paths, completion counts; invalid references rejected |
| 8 — FDE integration | Original content checksum retained; 27 chapters, 132 topics, 25 artifacts, 12 stages; learner state preserved |
| 9 — SEO/accessibility/performance | Canonicals, Open Graph, real social preview, JSON-LD, RSS, sitemap, labels, focus, contrast and responsive checks |
| 10 — Regression tests | Python, JavaScript search, and isolated Chromium suites passed; final command results below |
| 11 — Report and instructions | This report, exact file inventory, and [publishing instructions](../../content/README.md) |
| 12 — Final gate | Local acceptance checks completed; production deployment remains deliberately unperformed |

## Implemented behavior

- Publications overview, latest, all topics and individual topic pages, series,
  learning paths, dedicated article pages, and FDE entry route.
- Twelve configured technical domains and nine publication types. Additional
  categories and subcategories are configurable without application changes.
- Exactly one primary category, optional secondary categories, tags, author,
  difficulty, prerequisites, references, repositories, related publications,
  versions, and revision history. Reading time and TOC derive from content.
- Published/scheduled dates use ISO values; scheduled timestamps require a
  timezone. Unknown dates and optional metadata are not fabricated.
- Search across real content, with domain/type/difficulty/year/reading-time/
  series filters, relevance/latest/oldest/updated/alphabetical/recommended sorting,
  clear filters, empty states, and preserved query parameters.
- Separate article completion key: `technical-publications-completed-v1`.
  Opening an article does not complete it. FDE completion is read independently
  for collection progress and is never rewritten by the library.
- Safe technical rendering: highlighted code, tables, reference links, footnotes,
  inline/display math, lazy images, sanitized SVG diagrams, and restricted HTML.
- Public builds exclude unpublished routes, source files, private metadata
  relationships, search entries, feeds, and sitemap entries. Failed validation
  leaves the previous build intact; successful rebuilds remove stale routes.
- Archived publications retain their URLs with an explicit archive notice and
  leave discovery, search, RSS, and sitemap.

## Tests actually executed

From the repository root on Windows:

```powershell
.\.venv-site\Scripts\python.exe -m unittest discover -s tests/site -v
node --test tests/site/search.test.cjs
.\.venv-site\Scripts\python.exe scripts/publications.py validate
.\.venv-site\Scripts\python.exe scripts/publications.py build
.\.venv-site\Scripts\python.exe tests/site/make_browser_fixture.py
node --test tests/site/browser.test.cjs
node --check docs/assets/app.js
node --check docs/assets/publications.js
node --check docs/assets/publication-search.js
git diff --check
```

The browser command used `PLAYWRIGHT_MODULE` pointing to the pre-existing
Playwright 1.51.1 runtime, discovered from the installed browser registry. The
portable installation and environment-variable instructions are in
[the website README](../../docs/README.md).

Results:

| Check | Result |
| --- | --- |
| Python schema/content/build/authoring tests | 30 passed |
| JavaScript search/filter/sort tests | 10 passed |
| Chromium end-to-end scenarios | 7 passed |
| Public build | Passed; one real publication |
| JavaScript syntax | Passed |
| Metadata templates and workflow structure | Validated |
| Whitespace | Passed |
| Original FDE source | Byte-for-byte preserved locally; normalized checksum also recorded for Linux CI |

The first Python build-test run exposed three Windows default-encoding failures
in tests. Explicit UTF-8 reads fixed those failures; the rerun passed. No
pre-existing website functional failures were found in the baseline.

Browser scenarios cover the actual production artifact and isolated fixtures:

1. Library rendering, counts, routes, metadata, search, and original FDE entry.
2. New-article discovery, full-text search, composed filters and URL persistence.
3. Direct-URL, index, feed and sitemap exclusion for drafts/future entries;
   archived URL retention.
4. Article anchors, code, equations, tables, safe SVG, references, related items,
   explicit reading completion, series order, and learning paths.
5. FDE progress preserved byte-for-byte, including an unknown manually maintained
   state value, while navigating and completing a separate publication.
6. Layouts at 1440, 768, 390 and 320 px; mobile navigation, keyboard use, no
   horizontal overflow, and hosting beneath a project subpath.
7. Mobile article TOC, safe diagrams, and dark/light token contrast checks at
   least 4.5:1 for primary text, secondary text, and accent links.

Machine-readable browser outcomes: [browser-results.json](browser-results.json).
Visual artifacts are under `build/qa/`. Desktop/mobile library and article
screenshots were inspected. These are practical checks, not an independent
accessibility certification.

The FDE reader retains its original JavaScript and loads no new publication
index or article libraries. Its only presentation additions are a library link,
the associated link style, and canonical/social metadata in generated output.
Search indexes are generated once per build; browser requests do not rebuild
unchanged indexes. Large-catalog load testing was not performed.

## Content preservation

The original FDE file remains
`content/guides/end-to-end-fde-learning-map/README.md`. Its original working-tree
SHA-256 is `c181f453d66445927516ef13e4648c58915c4d6f2c214b246ccbbdcd59d034e9`.
The build copies its bytes unchanged into the reader's content asset.

The source contains 27 numbered chapters, 132 H2 topics (129 numbered topics
plus three priority headings), 25 portfolio artifacts, and 12 learning stages.
The existing 30 chapter/sidebar links, including orientation and roadmap entries,
remain driven by the original reader parser.

The original progress key `fde-field-guide-progress-v1`, chapter slugs, explicit
completion behavior, theme key, and learning sequence are retained. Tests run in
isolated browser contexts and never inspect or mutate the user's real browser
local storage. The guide's October 31, 2026 publication date comes from the
user's supplied brief; it is not an import timestamp. Unknown update date,
difficulty, and version were left unset.

## Exact file inventory for this extension

New:

- `requirements-site.txt`, `requirements-site-test.txt`
- `content/site.json`, `content/taxonomy.json`, `content/publication.schema.json`,
  `content/url-registry.json`
- `content/guides/end-to-end-fde-learning-map/publication.json`
- `content/series/fde-field-guide.json`
- `content/learning-paths/forward-deployed-engineering.json`
- `scripts/publication_model.py`, `scripts/publication_content.py`,
  `scripts/publication_views.py`, `scripts/build_publications.py`,
  `scripts/publications.py`, `scripts/serve_site.py`
- `docs/assets/publications.css`, `docs/assets/publications.js`,
  `docs/assets/publication-search.js`, `docs/assets/publications-social.png`
- `tests/site/test_model.py`, `tests/site/test_content.py`,
  `tests/site/test_build.py`, `tests/site/test_authoring.py`,
  `tests/site/search.test.cjs`, `tests/site/browser.test.cjs`,
  `tests/site/make_browser_fixture.py`
- `reports/publications/architecture.md`, `reports/publications/baseline.json`,
  `reports/publications/browser-results.json`, `reports/publications/implementation.md`

Updated:

- `.gitignore`: ignore the website environment and generated artifacts.
- `.github/workflows/deploy-fde-field-guide.yml`: validate/build/test the
  public-only artifact; deployment is gated by an explicit manual input.
- `docs/index.html`, `docs/assets/styles.css`: add the Publications link to FDE.
- `content/templates/article.md`, `content/templates/guide.md`: schema-compatible
  metadata templates.
- `content/README.md`, `content/articles/README.md`: automatic publishing workflow.
- `docs/README.md`, `README.md`, `CONTRIBUTING.md`: setup, safe preview, tests,
  source organization and deployment instructions.

Removed: none in this extension. Earlier repository reorganization changes
already existed before this task and remain uncommitted.

## Deployment and remaining limits

- No production deployment, repository commit, or push occurred.
- The canonical deployment target is explicitly configured in `content/site.json`.
  The live production URL and GitHub-hosted workflow have not been executed or
  independently verified in this local task.
- Scheduled content requires a new build after its timestamp, followed by an
  explicit deployment. No unattended scheduling has been configured or claimed.
- Markdown is supported. Arbitrary MDX/JavaScript embeds are deliberately not
  executed; interactive demonstrations can be linked as separate demos.
- Site-scale validation was performed with the current real publication and
  isolated fixtures, not with an invented public catalog or a large-scale load.

## Publish the next article

Use the exact commands and schema-compatible template in the
[publishing guide](../../content/README.md): create → edit → validate → private
preview → publish metadata with the real date → build → explicitly deploy when
ready. The local server is already running with content rebuilds enabled.
