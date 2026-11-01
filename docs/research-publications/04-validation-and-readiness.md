# Validation and production readiness

The public artifact builds successfully with 21 publications: the existing FDE guide and 20 numbered research articles. This task has not deployed the changes to production.

| Check | Result | Evidence |
|---|---|---|
| Metadata, publishing, rendering, and source regression tests | PASS — 36 Python tests | `python -m unittest discover -s tests/site -v` |
| Search and composed filters | PASS — 10 Node tests | `node --test tests/site/search.test.cjs` |
| Existing library and FDE browser regressions | PASS — 7 scenarios | `tests/site/browser.test.cjs`; `reports/publications/browser-results.json` |
| Research browser coverage | PASS — 2 scenarios covering all 20 pages | `tests/site/research.browser.test.cjs`; `build/qa/research-browser-results.json` |
| Source and public attachment preservation | PASS — 344 source files; zero failures | `source-manifest.json`, `preservation-audit.json` |
| Diagram rendering | PASS — 68 inline/supporting diagrams | All rendered in Chromium; 11 have explicit compatibility adaptations |
| Mathematics | PASS — 127 native MathML expressions across the research articles | Rendered article/browser counts; original LaTeX retained |
| Knowledge checks | PASS — 16 interactive checks and 4 reflections | Incorrect/correct responses and reset exercised for each multiple-choice check |
| Code copying | PASS | Actual clipboard interaction exercised on article 05 |
| Responsive reading and project hosting path | PASS — 1440, 768, 390, 320 pixels | Article 13, existing reader/library tests, and `/ai-systems-foundations/` browser routes |
| Production build | PASS | `python scripts/publications.py build` |
| Local links and file references in research pages | PASS — zero unresolved files/fragments | Preservation audit |

Five supplied standard-library lab suites ran successfully: 01 (3 tests), 04 (2), 10 (4), 11 (5), and 18 (4), totaling 18 lab tests. The runnable examples for 05 and 17 and the exact inline reality-gap example from 20 also exited successfully. Outputs are saved in `build/qa/research-lab-results.json`.

The Qiskit experiment in 14, PyTorch/accelerator experiments in 13, pandas exercise in 19, Lean proof in 12, and open-weight interpretability experiment in 08 were not executed in this environment. Their source code and dependencies are preserved, and student notes identify CPU/GPU/toolchain requirements. No clinical or biological experiment and no original research benchmark was reproduced.

## Performance and accessibility review

- Static HTML provides articles, references, navigation, and source transcripts without an application server. Knowledge-check explanations are available through native details elements when JavaScript is disabled.
- The 2.75 MB pinned Mermaid bundle is local and loaded only on research pages as diagrams approach the viewport. Rendering is serialized to avoid shared Mermaid registry conflicts.
- Source figures use local URLs, lazy loading in the body, and responsive sizing. Cover containers reserve space. Original PNG/SVG files are retained rather than recompressed, to protect source fidelity.
- Wide code, tables, equations, and diagrams scroll within their containers. The article grid permits shrinking on mobile. Expanded diagrams use a native dialog with a close button and Escape support.
- Quizzes use fieldsets, legends, radio labels, keyboard-accessible buttons, and live feedback. Copy buttons have text labels. Native details preserve keyboard access to source material.
- The existing dark/light token contrast checks continue passing. Automated checks do not constitute a full screen-reader or WCAG conformance audit.
- Full source text is indexed for search. No new package manager or server dependency is needed for normal builds; Mermaid is already vendored.

## Content and source qualifications

All supplied research text, figures, code, and references are preserved. Center-alignment wrappers are removed only while rendering Markdown; the stored source remains unchanged. Original transcripts may contain export artifacts and are available in full, in expandable text panels and downloads.

Eleven rendered diagrams use added quotation marks or line-break markup to make labels compatible with Mermaid 11. The original editable source is retained; affected figures also expose copyable working Mermaid. This is a documented rendering correction, not a claim that every original source block was valid unchanged.

Research organizations identify the subject or source of an article, not an affiliation or endorsement. Site dates represent this library edition. Public accessibility does not imply an open-source license. Supplied license notes and attribution files remain available; original sources retain their own terms.

Official source pages were checked selectively during implementation, including the original work on [monitoring](https://openai.com/index/chain-of-thought-monitoring/), [memory](https://openai.com/index/chatgpt-memory-dreaming/), [interpretability](https://www.anthropic.com/research/tracing-thoughts-language-model), [Project Swap](https://www.anthropic.com/research/project-swap), [formal verification](https://www.anthropic.com/research/formal-verification), [quantum circuits](https://www.anthropic.com/research/designing-efficient-quantum-circuits), [drug development](https://www.anthropic.com/research/early-progress-drug-development), [human judgment](https://www.anthropic.com/research/agents-judgment-calls), [AlphaEvolve](https://deepmind.google/blog/alphaevolve-impact/), [Genie 4](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/), [AlphaGenome Atlas](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/), and [Cosmos](https://research.nvidia.com/labs/cosmos-lab/cosmos-simulation/). This verifies selected reference availability and context; it is not exhaustive scientific peer review or independent replication. No external research figures were newly copied into the project.

Original external badges and fonts can require internet access. Locally hosted article figures, diagrams, and learning checks do not depend on a CDN. External reference availability can change after this review.

## Repeat the checks

```powershell
.\.venv-site\Scripts\python.exe -m unittest discover -s tests/site -v
node --test tests/site/search.test.cjs
.\.venv-site\Scripts\python.exe scripts/publications.py build
.\.venv-site\Scripts\python.exe scripts/audit_research.py
.\.venv-site\Scripts\python.exe tests/site/make_browser_fixture.py
$env:PLAYWRIGHT_MODULE = (Resolve-Path .venv-site/Lib/site-packages/playwright/driver/package).Path
$env:PLAYWRIGHT_BROWSERS_PATH = (Resolve-Path build/playwright-browsers).Path
node --test tests/site/browser.test.cjs tests/site/research.browser.test.cjs
```

This session installed browser binaries inside `build/playwright-browsers/`. On a fresh checkout, first install `requirements-site-test.txt`, set `PLAYWRIGHT_BROWSERS_PATH` to the desired local path, and run `python -m playwright install chromium` using the site virtual environment. CI installs its own Chromium.
