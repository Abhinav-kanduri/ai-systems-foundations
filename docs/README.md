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
node --test tests/site/browser.test.cjs
```

Tests use isolated browser contexts and fixture publications outside production
content. They verify source discovery, search/filter URLs, draft and future-date
protection, article rendering, series, progress isolation, and responsive layouts
at 1440, 768, 390, and 320 pixels. Screenshots go to `build/qa/`.

## Deployment

The [GitHub workflow](../.github/workflows/deploy-fde-field-guide.yml) validates
pushes and pull requests. It builds and tests the public artifact before upload.
Only a manual workflow dispatch with `deploy: true` runs the deployment job.
No production deployment was performed as part of local implementation.

Verify the intended production `siteUrl` in `content/site.json` before deployment.
It is the configured canonical target, not evidence of an existing live release.
Only `build/site/` is uploaded. Never upload `content/`, `build/preview/`, fixture
sources, or the repository root as a public site.

Scheduled content is included only when a build happens after its timestamp.
There is no unattended publishing scheduler.

## Source files

The author banner and external resource links are configured in
`content/site.json` under `authorBanner` and `resources`. The build copies the
configured banner from `assets/` into the public artifact. The library homepage
displays the banner. When resource links are configured, they appear throughout
the library and at the end of the original FDE reader. An empty `resources` list
hides the section.

- `index.html`, `assets/app.js`, `assets/styles.css`: existing curriculum reader.
- `assets/publications.css`: library and article styling using the same tokens.
- `assets/publications.js`: filters, theme, mobile navigation, reading progress.
- `assets/publication-search.js`: searchable, composable discovery logic.
- `../scripts/`: schema validation, content loader, build and authoring tools.

See the [architecture assessment](../reports/publications/architecture.md) and
[implementation report](../reports/publications/implementation.md).
