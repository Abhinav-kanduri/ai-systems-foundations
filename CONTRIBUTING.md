# Contributing

Contributions should explain reusable concepts, practical trade-offs, and system
behavior. Keep original educational material free of proprietary or confidential
information and do not redistribute paid course or book content.

## Where content belongs

| Content | Location |
| --- | --- |
| Concept explanation or learning lab | `foundations/<topic>/` |
| System design, cloud reference, or architecture diagram | `architectures/<system-or-platform>/` |
| Runnable application or project-specific guide | `projects/<project>/` |
| Blog or technical article | `content/articles/<slug>/README.md` |
| Long-form learning map, tutorial, or field guide | `content/guides/<slug>/README.md` |
| Career roadmap or Custom GPT configuration | `career/` |
| FDE website HTML, CSS, and JavaScript | `docs/` |
| Image shared across repository sections | `assets/images/` |

Keep datasets, models, notebooks, and outputs within the owning project.
Keep topic diagrams beside their documents. Create folders when content exists.

For authored blogs, technical articles, and guides, follow the
[writing conventions and templates](content/README.md). Keep the source and its
assets in one stable folder; track draft/review/published status in metadata.

## Naming and navigation

- Use lowercase folder names and kebab-case for new documentation files.
- Use `README.md` as a folder's entry point. Standard filenames such as
  `LICENSE`, `Dockerfile`, and `CONTRIBUTING.md` retain their conventional spelling.
- Preserve meaningful project asset names and numbered configuration files.
- Use relative links and update the relevant index when adding or moving material.
- Keep separate READMEs and dependency files for independent projects.
- Resolve application paths from the project location; avoid machine-specific absolute paths.
- Keep environments, caches, credentials, and local settings out of Git.
  Ignore rules do not untrack previously committed generated files.

## Checking changes

Check relative Markdown links and image paths after moves. For the website, serve
the repository root as described in [the website README](docs/README.md).
If the learning map moves, update both `docs/assets/app.js` and
`.github/workflows/deploy-fde-field-guide.yml`.

Run project-specific checks when changing application code. A documentation move
does not require retraining models or regenerating notebook outputs.

## Previous layout

| Previous path | Current path |
| --- | --- |
| `Generative_AI_lecture_notes/` | `foundations/generative-ai/` |
| `Large Language Model (LLM) Concepts/` | `foundations/llms/` |
| `Retrieval-Augmented Generation (RAG) Concepts/` | `foundations/rag/` |
| `AI Agent Concepts/` | `foundations/ai-agents/` |
| `Agentic AI Concepts/` | `foundations/agentic-ai/` |
| `MultiModel AI Concepts/` | `foundations/multimodal/` |
| `Architectures/` | `architectures/` (cloud material is under `cloud/`) |
| `DeepLearningProject/` | `projects/retail-customer-churn/` |
| `RAG-Project-v1/` | `projects/rag-pipeline/` |
| `reliable-multi-agent-loan-underwriting/` | `projects/reliable-multi-agent-loan-underwriting/` |
| `AI-Career/genai-career-navigator/` | `projects/genai-career-navigator/` |
| `AI-Career/` configuration files | `career/genai-career-navigator-gpt/` |
| `FordwardDeployementEngineer.md` | `content/guides/end-to-end-fde-learning-map/README.md` |
| `docs-preview.png` | `assets/images/fde-field-guide-preview.png` |
| Root and architecture `New Text Document.txt` files | `archive/placeholders/root.txt` and `archive/placeholders/architectures.txt` |

Topic overview files now use `README.md`; other foundation Markdown filenames use
kebab-case. The tokenizer lab is now `foundations/llms/tokenizer-lab.ipynb`.
