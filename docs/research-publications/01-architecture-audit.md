# Research publications architecture audit

The existing site uses a Python static build and plain HTML, CSS, and browser JavaScript. It does not use React, Next.js, MDX execution, or a Node application server. The research work extends this implementation and its navy/lime design tokens.

| Concern | Existing implementation | Research integration |
|---|---|---|
| Content | `content/articles/` and `content/guides/`, Markdown with frontmatter or `publication.json` sidecars | Twenty `research-problem-NN` directories; source README files remain unchanged |
| Discovery | `scripts/publication_content.py` | Validated research metadata and separately stored `learning.json` supplements |
| Validation | `scripts/publication_model.py`, `content/publication.schema.json` | Number, organization, cover, and inventoried package-file fields |
| Rendering | Python-Markdown, Bleach, Pygments, latex2mathml | Native MathML for dollar and backslash delimiters; trusted diagram containers; preserved LaTeX |
| Page templates | `scripts/publication_views.py` | Student introductions, source disclosures, covers, knowledge checks, and series overview |
| Design | `docs/assets/styles.css` and `publications.css` | Token-based additions in `research.css`; original global styles retained |
| Browser behavior | `docs/assets/publications.js`, `publication-search.js` | `research-reader.js` supplies code copying, local quizzes, lazy Mermaid rendering, and expanded diagrams |
| Search | Source-driven `publications/index.json`, composable filters | All research articles indexed; research organization and series titles searchable |
| Collections | `content/series/*.json`, `content/learning-paths/*.json` | One ordered series and three student paths; existing FDE collection remains |
| Artifact | `scripts/build_publications.py`, output `build/site/` | Only inventoried source attachments published; active HTML examples served as plain text |
| Local server | `scripts/publications.py serve`, `scripts/serve_site.py` | Existing loopback preview and request-triggered rebuilds |
| Deployment | `.github/workflows/deploy-fde-field-guide.yml` | Research browser tests added; no production deployment performed for this task |
| Tests | Python unittest and Node test runner with Playwright | Source-byte checks, renderer checks, all-article browser coverage, and preservation audit |

The input directory contains 20 ZIP packages. Initial import uses `scripts/import_research.py`; `scripts/research_supplements.py` creates separate student additions. Both commands refuse to overwrite article content. Subsequent builds use the committed content, not the ignored ZIPs.

`source-manifest.json` is the source preservation baseline. `scripts/audit_research.py` compares all imported file bodies and the generated attachments. `.gitattributes` disables newline conversion for the research packages so their hashes remain stable across platforms.

Mermaid 11.12.0 is vendored from the official npm package with its MIT license under `docs/assets/vendor/mermaid/`. It loads from the same site only when a diagram approaches the viewport. No student answer is sent to an external service.

Original publication records, FDE Markdown, curriculum fragments, and the `fde-field-guide-progress-v1` storage key were retained. Existing uncommitted edits were preserved on `feature/research-to-reality-20-articles`.
