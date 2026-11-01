# AI Systems Foundations

Core concepts, architecture notes, and hands-on projects for understanding how AI
systems behave in production: language models, retrieval, agents, evaluation,
reliability, and enterprise deployment.

The learning material focuses on system design, practical trade-offs, and failure
modes. The projects provide examples to explore alongside those concepts.

## Start here

1. Build the basics with [Generative AI and deep learning](foundations/generative-ai/README.md).
2. Study [language models](foundations/llms/README.md) and [tokenization](foundations/llms/tokenization.md).
3. Follow the [RAG learning sequence](foundations/rag/README.md).
4. Explore [AI agents](foundations/ai-agents/README.md), [agentic AI](foundations/agentic-ai/README.md), and [multimodal AI](foundations/multimodal/README.md).
5. Review [system architectures](architectures/README.md) and choose a [project](projects/README.md).
6. Read or write [blogs, technical articles, and learning guides](content/README.md).

## Repository structure

```text
ai-systems-foundations/
├── foundations/                 Concept notes and learning notebooks
│   ├── generative-ai/
│   ├── llms/
│   ├── rag/
│   ├── ai-agents/
│   ├── agentic-ai/
│   └── multimodal/
├── architectures/               System designs and architecture diagrams
│   ├── cloud/                   AWS, Azure, Google Cloud, Databricks
│   ├── production-llm-system/
│   └── rag/
├── projects/                    Applications and project guides
│   ├── genai-career-navigator/
│   ├── rag-pipeline/
│   ├── reliable-multi-agent-loan-underwriting/
│   └── retail-customer-churn/
├── content/                     Blogs, technical articles, and learning guides
│   ├── articles/
│   ├── guides/
│   └── templates/
├── career/                      Career resources and Custom GPT configuration
├── docs/                        FDE Field Guide website (GitHub Pages)
├── assets/images/               Repository-wide images
├── archive/placeholders/        Preserved empty placeholder files
├── .github/workflows/           Deployment automation
├── scripts/                     Publication build, authoring, and local server
├── tests/site/                  Metadata, publishing, search, and browser tests
├── reports/publications/        Architecture, baseline, and implementation report
├── CONTRIBUTING.md              Organization and contribution conventions
├── LICENSE
└── README.md
```

| Area | Contents |
| --- | --- |
| [Foundations](foundations/README.md) | Concepts, lecture notes, and a tokenizer lab |
| [Architectures](architectures/README.md) | Cloud platforms, production LLM systems, and RAG validation |
| [Projects](projects/README.md) | Churn prediction, career dashboard, loan underwriting, and a RAG pipeline guide |
| [Writing library](content/README.md) | Blogs, technical articles, learning guides, and reusable writing templates |
| [Career](career/README.md) | Career resources and the GenAI Career Navigator Custom GPT package |
| [Website](docs/README.md) | FDE Field Guide source, local preview, and deployment instructions |

## Working with projects

Each project owns its dependencies, data, configuration, and run instructions.
Open its README and run commands from that project's directory. For example:

```powershell
cd projects/genai-career-navigator
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The [RAG pipeline](projects/rag-pipeline/README.md) is a setup guide and design
reference; its proposed application files are not yet implemented.

To run the publications platform and FDE website from the repository root:

```powershell
python -m venv .venv-site
.\.venv-site\Scripts\python.exe -m pip install -r requirements-site.txt
.\.venv-site\Scripts\python.exe scripts/publications.py serve --port 8000
```

Open <http://localhost:8000/publications/> for the library or
<http://localhost:8000/docs/> for the original FDE reader. The local server
rebuilds changed content and serves only the generated public artifact.

See [publishing instructions](content/README.md) to add the next article and
[website documentation](docs/README.md) for tests and deployment.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for folder placement, naming conventions,
and a map from the previous layout. Keep explanations reusable, diagrams beside
the material they describe, and project implementation inside projects.

## Author and license

**Abhinav Kanduri** · [LinkedIn](https://www.linkedin.com/in/abhinav-kanduri-a943b9353/)

Licensed under the [MIT License](LICENSE).

This repository is for educational and research purposes. It reflects the
author's personal views and is not affiliated with an employer, client, or
organization. Examples are illustrative and use publicly available knowledge or
generalized practices; no proprietary, confidential, or client-specific material
is intended for inclusion.
