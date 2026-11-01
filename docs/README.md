# Publications website and original FDE reader

The original HTML/CSS/JavaScript FDE reader remains here. A Python build extends
it with a Technical Publications library, article pages, topic indexes, series,
learning paths, full-text search data, RSS, and sitemap.

## Local development

From the repository root:

```powershell
python -m venv .venv-site
.\.venv-site\Scripts\python.exe -m pip install -r requirements-site.txt
.\.venv-site\Scripts\python.exe scripts/publications.py serve --port 8000
```

- [Technical Publications](http://localhost:8000/publications/)
- [Research to Reality: 20 AI research problems](http://localhost:8000/publications/series/research-to-reality/)
- [Original FDE reader](http://localhost:8000/docs/#end-to-end-fde-learning-map)
- [RSS](http://localhost:8000/publications/feed.xml)
- [Sitemap](http://localhost:8000/sitemap.xml)

The server watches content and presentation files and rebuilds on the next
request. It binds only to loopback and serves `build/site/`. Source directories,
drafts, templates, credentials, and Git metadata are not exposed.

Read the [publishing guide](../content/README.md) to add or preview an article.
The [original FDE source](../content/guides/end-to-end-fde-learning-map/README.md)
remains unchanged. Its existing fragments and `fde-field-guide-progress-v1`
completion storage are preserved.

## Validation and production build

```powershell
.\.venv-site\Scripts\python.exe scripts/publications.py validate
.\.venv-site\Scripts\python.exe -m unittest discover -s tests/site -v
node --test tests/site/search.test.cjs
.\.venv-site\Scripts\python.exe scripts/publications.py build
```

Public output is `build/site/`. A successful build atomically replaces the prior
artifact, removing routes that are no longer public. A failed validation retains
the last good artifact.

For browser regression tests, install the optional test tools and Chromium:

```powershell
.\.venv-site\Scripts\python.exe -m pip install -r requirements-site-test.txt
.\.venv-site\Scripts\python.exe -m playwright install chromium
.\.venv-site\Scripts\python.exe tests/site/make_browser_fixture.py
$env:PLAYWRIGHT_MODULE = (Resolve-Path .venv-site/Lib/site-packages/playwright/driver/package).Path
node --test tests/site/browser.test.cjs tests/site/research.browser.test.cjs
```

Tests use isolated browser contexts and fixture publications outside production
content. They verify source discovery, search/filter URLs, draft and future-date
protection, article rendering, series, progress isolation, and responsive layouts
at 1440, 768, 390, and 320 pixels. Screenshots go to `build/qa/`.

The research suite also visits all 20 articles, renders every inline and
supporting Mermaid diagram, checks interactive answers and reset behavior,
exercises code copying, and follows the series under a GitHub Pages subpath.
For a complete source and public-file preservation audit, run a build followed
by `.\.venv-site\Scripts\python.exe scripts/audit_research.py`.
See [the research implementation report](research-publications/FINAL-IMPLEMENTATION-REPORT.md)
for source coverage, validation evidence, and optional lab requirements.

## Deployment

The [GitHub workflow](../.github/workflows/deploy-fde-field-guide.yml) validates
pushes and pull requests. It builds and tests the public artifact before upload.
Successful site changes pushed to `main` deploy automatically. Pull requests
only validate. A manual workflow dispatch on `main` with `deploy: true` can
redeploy; leaving it unchecked runs validation only.

In [repository Settings → Pages](https://github.com/Abhinav-kanduri/ai-systems-foundations/settings/pages),
set **Build and deployment → Source** to **GitHub Actions**. Use this workflow
as the only Pages publisher. The generic Jekyll workflow builds the repository
root and publishes the README instead of the generated website.

After merging to `main`, wait for both `verify` and `deploy` in
[Actions](https://github.com/Abhinav-kanduri/ai-systems-foundations/actions/workflows/deploy-fde-field-guide.yml)
to succeed, then check:

- [FDE Field Guide](https://abhinav-kanduri.github.io/ai-systems-foundations/)
- [Technical Publications](https://abhinav-kanduri.github.io/ai-systems-foundations/publications/)
- [RSS](https://abhinav-kanduri.github.io/ai-systems-foundations/publications/feed.xml)
- [Sitemap](https://abhinav-kanduri.github.io/ai-systems-foundations/sitemap.xml)

Verify chapter navigation, library search, and the link back to the guide. If
the README still appears, check that no other workflow deploys a Jekyll build.

Verify the intended production `siteUrl` in `content/site.json` before deployment.
It is the configured canonical target, not evidence of an existing live release.
Only `build/site/` is uploaded. Never upload `content/`, `build/preview/`, fixture
sources, or the repository root as a public site.

Scheduled content is included only when a build happens after its timestamp.
There is no unattended publishing scheduler.

## Source files

The author banner is configured in `content/site.json` under `authorBanner`.
The build copies it from `assets/` into the public artifact and displays it on
the library homepage and at the end of the original FDE reader.
The homepage introduction and shared educational note are configured under
`heroSubtitle` and `editorialNote` in the same file.
The note includes the community website and newsletter links. The full welcome
message is stored in `content/about.md` and rendered at `/publications/about/`.

- `index.html`, `assets/app.js`, `assets/styles.css`: existing curriculum reader.
- `assets/publications.css`: library and article styling using the same tokens.
- `assets/publications.js`: filters, theme, mobile navigation, reading progress.
- `assets/publication-search.js`: searchable, composable discovery logic.
- `../scripts/`: schema validation, content loader, build and authoring tools.

See the [architecture assessment](../reports/publications/architecture.md) and
[implementation report](../reports/publications/implementation.md).
