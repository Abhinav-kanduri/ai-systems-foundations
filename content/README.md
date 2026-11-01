# Technical Publications: writing and publishing

The website discovers publications from Markdown metadata. Adding content updates
article pages, latest publications, search, topic counts, feeds, and sitemap at
build time. You do not edit frontend components or navigation lists for each post.

## Run locally

From the repository root on Windows:

```powershell
python -m venv .venv-site
.\.venv-site\Scripts\python.exe -m pip install -r requirements-site.txt
.\.venv-site\Scripts\python.exe scripts/publications.py serve --port 8000
```

Open <http://localhost:8000/publications/>. The original FDE guide is available
at <http://localhost:8000/docs/#end-to-end-fde-learning-map>. The local server
rebuilds changed content on the next request and serves only `build/site/`.

## Write the next article

```powershell
.\.venv-site\Scripts\python.exe scripts/publications.py new "Understanding GPU Memory" --category gpu --type technical-article
```

This creates `content/articles/understanding-gpu-memory/README.md` with a stable
publication ID, URL slug, valid draft metadata, and an outline. Edit its title,
summary, metadata, and body. The command prints the new ID; use that ID or the
slug in subsequent commands.

```powershell
.\.venv-site\Scripts\python.exe scripts/publications.py validate
.\.venv-site\Scripts\python.exe scripts/publications.py preview understanding-gpu-memory --port 8002
```

The preview command prints the article URL. It serves a separate loopback-only
`build/preview/` artifact with `noindex` metadata. Drafts remain absent from the
public build. Stop that preview server with Ctrl+C when finished.

To publish, supply the actual original publication date or timestamp:

```powershell
.\.venv-site\Scripts\python.exe scripts/publications.py publish understanding-gpu-memory --at YYYY-MM-DD
.\.venv-site\Scripts\python.exe scripts/publications.py build
```

Replace `YYYY-MM-DD` with the real date. This updates metadata and registers the
permanent URL; it does not deploy. A future publication requires a full timestamp
with timezone, for example `2026-11-01T09:00:00-07:00`, and gets `scheduled` status.

## Content structure

```text
content/
├── articles/<slug>/README.md         Focused blogs and technical articles
├── guides/<slug>/README.md           Tutorials, learning maps, field guides
├── guides/end-to-end-fde-learning-map/
│   ├── README.md                     Original FDE text, unchanged
│   └── publication.json              Metadata without modifying that text
├── templates/                        Article and guide starting points
├── series/*.json                     Explicit ordered publication collections
├── learning-paths/*.json             Cross-topic ordered reading paths
├── taxonomy.json                     Categories, optional parentId, and types
├── publication.schema.json           Validated metadata contract
├── site.json                         Site identity and canonical deployment base
└── url-registry.json                 Locked published IDs, slugs, canonical URLs
```

Each piece can have its own `assets/` and `examples/` directories. Use relative
links such as `assets/retrieval-flow.svg`. These files are copied only for
publicly available publications. Create folders when they contain files.

## Metadata template

Use the [article](templates/article.md) or [guide](templates/guide.md) template.
This minimal frontmatter matches the implemented schema:

```yaml
---
id: a-stable-unique-id
slug: understanding-gpu-memory
title: "Understanding GPU Memory"
summary: "Replace this with the article's actual scope and conclusion."
author: "Abhinav Kanduri"
primaryCategory: gpu
secondaryCategories: []
publicationType: technical-article
status: draft
publishedAt: null
updatedAt: null
tags: []
technologies: []
difficulty: null
prerequisites: []
seriesId: null
relatedPublicationIds: []
repositoryLinks: []
researchReferences: []
canonicalUrl: null
---
```

Required fields are `id`, `title`, `summary`, `primaryCategory`, `publicationType`,
and `status`. Slugs derive from the title when omitted; explicit stable slugs are
recommended. Published, scheduled, and archived records require `publishedAt`.
Reading time and table of contents derive from the actual content. Unknown
subtitle, difficulty, version, update dates, prerequisites, and references remain
optional. Never substitute import time for the original publication date.

## Editorial lifecycle and URLs

- Move from `draft` → `review` → `scheduled` or `published` → `archived` by editing
  metadata or using the publish command. Keep the same source folder throughout.
- Draft/review content and future-scheduled content have no public routes, cards,
  search entries, feed items, or sitemap entries.
- Scheduling is evaluated at build time using timezone-qualified timestamps.
  There is no unattended scheduler configured. Rebuild and explicitly deploy
  after the intended time; a scheduled source file alone does not publish itself.
- An archive keeps its article URL with an archive notice and leaves discovery,
  feeds, and sitemap. Do not delete a formerly published source to archive it.
- The publish command locks published URLs in `url-registry.json`. Slug or
  canonical changes then fail validation. Keep the original URL unless you
  deliberately implement and verify a redirect migration.
- Retain `publishedAt` for revisions. Set `updatedAt`, optionally add `version`
  and `revisions` entries, and use Git for full revision history.
- `canonicalUrl` defaults to the configured site URL plus the article route. The
  FDE record keeps the original curriculum URL as its canonical reading location.

## Topics, related articles, series, and learning paths

Add categories and types in `taxonomy.json`; no application edits are required.
Each publication has one `primaryCategory`, optional `secondaryCategories`, and
tags. Subcategories can reference a configured `parentId`.

Use actual publication IDs in `relatedPublicationIds`. A series or path JSON
file has `id`, `slug`, `title`, `description`, `status`, and an ordered
`publicationIds` array. Only available members appear in public navigation.
Series order comes from that array; optional article `seriesId`/`seriesOrder`
must agree with it. Reading completion requires an explicit user action.

## Rendering and deployment

Markdown supports tables, fenced code with syntax highlighting, images and SVG
diagrams, reference links, footnotes, and inline `$...$` or display `$$` LaTeX
converted to native MathML. Active HTML is sanitized. MDX execution and embedded
scripts are not supported. Interactive demos should be linked as external demos.

Review [website checks and deployment](../docs/README.md) and the
[implementation report](../reports/publications/implementation.md).
