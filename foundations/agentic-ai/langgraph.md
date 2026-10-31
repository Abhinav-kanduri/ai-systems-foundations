# LangGraph for Production-Grade Agentic AI

Build stateful, reliable, multi-step LLM agents using **LangGraph** for production-ready Agentic RAG workflows.

---

## Overview

This repository contains a hands-on learning project for building a **production-grade Agentic RAG Compliance Assistant** with LangGraph.

The project demonstrates how to design, implement, evaluate, and deploy a stateful AI agent that can:

- Retrieve documents
- Call tools
- Make decisions
- Maintain workflow state
- Route risky outputs to human review
- Recover from failures
- Trace and evaluate agent behavior

LangGraph is used as the orchestration layer for building long-running, stateful, multi-step LLM workflows.

---

## Problem Statement

Enterprises increasingly want AI agents that can go beyond simple chat responses.

A production-grade AI agent may need to:

- Research across documents
- Retrieve evidence
- Call external tools
- Make conditional decisions
- Ask humans for approval
- Resume after failures
- Maintain memory
- Provide audit-ready traces

Basic `LLM + tools` loops are often brittle. They may lose state, repeat expensive steps after crashes, call unsafe tools, or become difficult to debug.

This project solves that problem by modeling the agent as a **stateful graph**, where each node performs a specific task and checkpoints preserve execution state.

---

## Solution Overview

The project implements an **Agentic RAG Compliance Assistant**.

The assistant answers compliance-related questions from policy documents, verifies whether answers are grounded in retrieved evidence, and routes risky or low-confidence outputs to a human reviewer.

LangGraph enables the workflow to be represented as an explicit graph:

```text
User Question
   ↓
Input Classifier
   ↓
Query Planner
   ↓
Retriever
   ↓
Answer Generator
   ↓
Citation Verifier
   ↓
Risk Classifier
   ↓
Human Approval, if required
   ↓
Final Response
   ↓
Tracing + Evaluation
```

---

## Key Features

* Stateful multi-step agent workflow
* Agentic RAG over policy documents
* Tool-calling support
* Retrieval with citations
* Conditional routing
* Human-in-the-loop approval
* Confidence scoring
* Citation verification
* Durable execution with checkpoints
* Workflow replay and recovery
* Observability with LangSmith or Langfuse
* Evaluation for faithfulness, retrieval quality, tool use, and escalation accuracy

---

## Architecture

```text
User / App UI
   ↓
FastAPI or Streamlit Interface
   ↓
LangGraph Orchestration Layer
   ↓
Planner ─ Retriever ─ Generator ─ Verifier ─ Risk Classifier
   ↓
LLM + Tools + Vector Database + Memory
   ↓
Observability + Evaluation + Governance
```

---

## Core Concepts

### LangGraph

LangGraph is an orchestration framework for building stateful, multi-step, agentic workflows.

Instead of implementing an uncontrolled agent loop, LangGraph lets developers define:

| Component         | Purpose                                               |
| ----------------- | ----------------------------------------------------- |
| State             | Shared data passed between workflow steps             |
| Nodes             | Functions or agents that perform work                 |
| Edges             | Transitions between nodes                             |
| Conditional Edges | Dynamic routing based on state                        |
| Tools             | External APIs, search, databases, or business systems |
| Checkpointer      | Persistence layer for recovery                        |
| Human Interrupts  | Pause points for review or approval                   |
| Tracing           | Observability for debugging and evaluation            |

---

## Example Use Case

A user asks:

```text
How long should employees retain financial records?
```

The system should return:

```text
Answer:
Employees must retain financial records for X years according to the policy.

Citations:
- Policy Section 4.2
- Compliance Handbook Page 17

Confidence:
High

Review Required:
No
```

For sensitive, uncertain, or poorly cited answers, the workflow routes to human approval before returning a final response.

---

## Tech Stack

| Layer           | Tool                                                  |
| --------------- | ----------------------------------------------------- |
| Orchestration   | LangGraph                                             |
| LLM             | OpenAI, Anthropic, Gemini, Llama, or Mistral          |
| Embeddings      | OpenAI Embeddings, BGE, E5, or Instructor             |
| Vector Database | Chroma, Qdrant, Pinecone, Weaviate, or pgvector       |
| Backend         | Python + FastAPI                                      |
| UI              | Streamlit or React                                    |
| Observability   | LangSmith or Langfuse                                 |
| Evaluation      | Ragas, DeepEval, LangSmith Evals                      |
| Deployment      | Docker, Kubernetes, serverless, or LangGraph Platform |

---

## Project Structure

```text
.
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── edges.py
│   │   └── workflow.py
│   ├── ingestion/
│   │   ├── loaders.py
│   │   ├── chunking.py
│   │   └── embeddings.py
│   ├── retrieval/
│   │   └── retriever.py
│   ├── evaluation/
│   │   └── evaluators.py
│   ├── tools/
│   │   └── compliance_tools.py
│   └── config.py
├── data/
│   ├── raw/
│   └── processed/
├── tests/
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Workflow Design

### State Definition

Example LangGraph state:

```python
from typing import TypedDict, List, Optional

class ComplianceAgentState(TypedDict):
    query: str
    planned_steps: List[str]
    retrieved_docs: List[dict]
    answer_draft: Optional[str]
    citations: List[str]
    confidence: Optional[str]
    risk_level: Optional[str]
    review_required: bool
    human_feedback: Optional[str]
    final_answer: Optional[str]
```

---

## Graph Nodes

| Node              | Responsibility                                        |
| ----------------- | ----------------------------------------------------- |
| Input Classifier  | Detects query type, sensitivity, and intent           |
| Query Planner     | Breaks the question into retrieval or reasoning steps |
| Retriever         | Fetches relevant document chunks                      |
| Answer Generator  | Produces a grounded draft answer                      |
| Citation Verifier | Checks whether citations support the answer           |
| Risk Classifier   | Determines whether human review is required           |
| Human Approval    | Pauses workflow for reviewer input                    |
| Final Responder   | Returns the final answer to the user                  |

---

## Conditional Routing

Example routing logic:

| Condition         | Route             |
| ----------------- | ----------------- |
| Low confidence    | Retrieve again    |
| Missing citation  | Regenerate answer |
| Sensitive topic   | Human approval    |
| Unsupported claim | Verifier retry    |
| Approved response | Final responder   |

---

## Installation

### Prerequisites

* Python 3.10+
* API key for your chosen LLM provider
* Vector database, such as Chroma, Qdrant, Pinecone, Weaviate, or pgvector
* Optional: LangSmith or Langfuse account for tracing

### Clone the Repository

```bash
git clone https://github.com/your-org/langgraph-agentic-rag-compliance-assistant.git
cd langgraph-agentic-rag-compliance-assistant
```

### Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Example configuration:

```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-compliance-assistant

VECTOR_DB_PROVIDER=chroma
VECTOR_DB_PATH=./data/vectorstore

APP_ENV=development
```

| Variable               | Description                   | Required                     |
| ---------------------- | ----------------------------- | ---------------------------- |
| `OPENAI_API_KEY`       | API key for OpenAI models     | Yes, if using OpenAI         |
| `LANGCHAIN_API_KEY`    | API key for LangSmith tracing | Optional                     |
| `LANGCHAIN_TRACING_V2` | Enables LangSmith tracing     | Optional                     |
| `LANGCHAIN_PROJECT`    | LangSmith project name        | Optional                     |
| `VECTOR_DB_PROVIDER`   | Vector database provider      | Yes                          |
| `VECTOR_DB_PATH`       | Local vector database path    | Required for local vector DB |
| `APP_ENV`              | Runtime environment           | Optional                     |

---

## Data Ingestion

Place policy documents in:

```text
data/raw/
```

Supported formats can include:

* PDF
* Markdown
* Text
* HTML
* DOCX, if configured

Run ingestion:

```bash
python -m app.ingestion.load_documents
```

The ingestion pipeline should:

1. Load documents
2. Split them into chunks
3. Generate embeddings
4. Store chunks in a vector database
5. Preserve metadata for citation tracking

---

## Running the Application

### Run the API

```bash
uvicorn app.api.routes:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### Run the UI

If using Streamlit:

```bash
streamlit run app/ui/main.py
```

If using React:

```bash
npm install
npm run dev
```

---

## Example API Usage

### Ask a Compliance Question

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How long should employees retain financial records?"
  }'
```

Example response:

```json
{
  "answer": "Employees must retain financial records for X years according to the company retention policy.",
  "citations": [
    "Policy Section 4.2",
    "Compliance Handbook Page 17"
  ],
  "confidence": "high",
  "review_required": false
}
```

---

## Evaluation Metrics

| Metric              | Meaning                                               |
| ------------------- | ----------------------------------------------------- |
| Answer Faithfulness | Whether the answer is grounded in retrieved documents |
| Citation Accuracy   | Whether citations support the generated answer        |
| Retrieval Precision | Whether retrieved chunks are relevant                 |
| Tool Accuracy       | Whether the agent selected the correct tools          |
| Escalation Accuracy | Whether risky cases were routed to human review       |
| Latency             | End-to-end response time                              |
| Cost                | Total model and tool-call cost                        |
| Recovery Success    | Whether the workflow can resume after failure         |

---

## Observability

The project can integrate with LangSmith or Langfuse to track:

* User inputs
* LLM calls
* Tool calls
* Retrieved documents
* Token usage
* Latency
* Cost
* Errors
* Intermediate state
* Evaluation results

This helps debug agent behavior and identify failures such as:

* Incorrect retrieval
* Unsupported citations
* Tool misuse
* Repeated loops
* High-cost execution paths
* Poor escalation decisions

---

## Security and Governance

Production agentic systems should include controls for:

| Risk                   | Control                                  |
| ---------------------- | ---------------------------------------- |
| Unsafe tool calls      | Policy node before execution             |
| Sensitive data leakage | PII redaction before logging             |
| Hallucinated answers   | Retrieval-grounded verification          |
| Unauthorized actions   | Human approval node                      |
| Prompt injection       | Input sanitization and tool boundaries   |
| Cost explosion         | Step limits, timeouts, and model routing |

---

## Production Considerations

For production deployment, consider:

* Persistent checkpointer storage
* Idempotent tool calls
* Retry policies
* Timeout limits
* Human approval queues
* Role-based access control
* Secrets management
* Audit logging
* Monitoring and alerting
* Cost tracking
* Evaluation regression tests

---

## Deployment

### Docker

Build the image:

```bash
docker build -t langgraph-compliance-assistant .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 langgraph-compliance-assistant
```

### Kubernetes

For Kubernetes deployments, add:

* Deployment manifest
* Service manifest
* ConfigMap
* Secret
* Persistent storage for checkpoints
* Horizontal autoscaling rules

---

## Roadmap

* [ ] Add document ingestion pipeline
* [ ] Add LangGraph state and workflow nodes
* [ ] Add vector database integration
* [ ] Add citation verifier
* [ ] Add human approval workflow
* [ ] Add LangSmith tracing
* [ ] Add evaluation suite
* [ ] Add FastAPI service
* [ ] Add Streamlit or React UI
* [ ] Add Docker deployment
* [ ] Add production checkpointer
* [ ] Add role-based governance controls

---

## Related Frameworks

| Framework   | Best Fit                                            |
| ----------- | --------------------------------------------------- |
| LangGraph   | Stateful, production-grade agent orchestration      |
| LangChain   | LLM chains, tools, integrations, and RAG components |
| CrewAI      | Role-based multi-agent workflows                    |
| AutoGen     | Conversational multi-agent research workflows       |
| Pydantic AI | Type-safe Python agent development                  |
| LlamaIndex  | RAG-first document intelligence systems             |

---

## Learning Agenda

This project supports a webinar or workshop covering:

1. Why agentic AI needs orchestration beyond simple chains
2. LangGraph fundamentals: state, nodes, edges, and graphs
3. Building a single-agent workflow
4. Adding tools, retrieval, and routing
5. Multi-agent patterns: planner, researcher, verifier, executor
6. Durable execution, checkpoints, replay, and time travel
7. Human-in-the-loop approval and governance
8. Observability and evaluation
9. Production architecture and deployment
10. Hands-on project walkthrough

---

## Interview Topics

### Beginner

* What is Agentic AI?
* How is an agent different from a chatbot?
* What are tools in an LLM agent?
* What is the difference between a chain and a graph?
* Why do agents need memory?

### Intermediate

* What problem does LangGraph solve?
* Explain nodes, edges, state, and conditional routing.
* How does Agentic RAG differ from traditional RAG?
* Why is durable execution important?
* How would you prevent unsafe tool calls?

### Advanced

* How would you design a planner-researcher-verifier-executor workflow?
* What are the trade-offs between LangGraph and CrewAI?
* How do checkpoints enable replay and time travel?
* How would you evaluate tool-use correctness?
* What are common failure modes in long-running agents?

### System Design

* Design a LangGraph-based customer support agent for a bank.
* Design an Agentic RAG system with human approval for legal documents.
* How would you support retries, state recovery, and audit logs?
* How would you separate orchestration, retrieval, memory, and tools?
* How would you deploy LangGraph agents at enterprise scale?

---

## Assumptions

This README assumes:

* Python is the primary implementation language.
* LangGraph is used as the orchestration layer.
* A vector database is used for retrieval.
* The project supports either LangSmith or Langfuse for observability.
* The LLM provider is configurable.
* Human review is required for sensitive or low-confidence answers.

Update these assumptions based on your final implementation.

---

## Contributing

Contributions are welcome.

Suggested workflow:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes

```bash
git commit -m "Add your feature"
```

4. Push to your branch

```bash
git push origin feature/your-feature-name
```

5. Open a pull request

Please include tests, documentation updates, and example usage where relevant.

---

## License

This project is available under the MIT License.

Update this section if your organization uses a different license.

---

## Maintainer

Maintained by:

```text
Abhinav Kanduri
```

For questions, issues, or feature requests, open an issue in the repository.

```
abhinav.kanduri01@gmail.com
```
