# Reliable Multi-Agent Loan Underwriting System

## Overview

This project demonstrates a **production-grade multi-agent AI workflow** for evaluating loan applications. It serves as a comprehensive reference implementation combining:

- **Specialized AI agents** for different underwriting concerns
- **Durable workflow orchestration** with state management
- **Immutable evidence logging** for auditability
- **Idempotent execution** for reliability
- **Human-in-the-loop governance** for high-risk decisions
- **OpenTelemetry observability** for tracing and monitoring

## What's Included

### Code Implementation

✅ **Agent System** (7 specialized agents)
- DocumentIntakeAgent: Parses documents, extracts fields
- IncomeVerificationAgent: Verifies income from multiple sources
- CreditScoringAgent: Evaluates credit risk
- FraudDetectionAgent: Detects fraud signals
- ComplianceAgent: Checks regulatory compliance
- RiskAssessmentAgent: Aggregates evidence, assigns risk level
- FinalApprovalAgent: Makes approval/rejection decision

✅ **Orchestration Engine**
- State machine with 12 workflow states
- Parallel agent execution (4 agents run concurrently)
- Checkpoint-based recovery
- Workflow state versioning

✅ **Data Schemas** (Pydantic models)
- Application intake schemas
- Evidence logging structures
- Agent input/output contracts
- Decision records
- Workflow state management

✅ **FastAPI Application**
- Application submission endpoints
- Workflow status monitoring
- Decision retrieval with evidence
- Human review workflow
- Trace and audit endpoints

✅ **Configuration**
- Docker Compose for local development
- Dockerfile for containerization
- Environment variable configuration
- pyproject.toml and requirements.txt

✅ **Testing & Evaluation**
- Unit tests for agents
- Integration tests for workflow
- Evaluation suite with golden dataset
- Decision accuracy testing
- Consistency validation

✅ **Documentation**
- README with quick start
- Architecture guide with diagrams
- Deployment guide (local, Docker, Kubernetes, AWS)
- API reference
- .gitignore for version control

## Directory Structure

```
reliable-multi-agent-loan-underwriting/
├── api/                              # FastAPI application
│   ├── main.py                       # App factory
│   └── routes/                       # API endpoints (4 routers)
├── agents/                           # 7 specialized agents
├── orchestrator/                     # Workflow orchestration
├── schemas/                          # Pydantic models (6 modules)
├── storage/                          # Data persistence (skeleton)
├── observability/                    # Tracing & logging (skeleton)
├── tests/                            # Test suite (unit, integration)
├── evals/                            # Evaluation suite
├── docs/                             # Architecture & deployment guides
├── docker-compose.yml                # Full stack setup
├── Dockerfile                        # Container image
├── pyproject.toml                    # Project metadata
├── requirements.txt                  # Dependencies
└── README.md                         # Main documentation
```

## Quick Start

### Local Development

```bash
# Clone and setup
git clone <repo>
cd reliable-multi-agent-loan-underwriting
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run API
uvicorn api.main:app --reload
# Open http://localhost:8000/docs
```

### Docker Compose

```bash
# Start all services
docker-compose up --build

# Services available:
# - API: http://localhost:8000
# - UI: http://localhost:8501
# - Jaeger: http://localhost:16686
# - Database: localhost:5432
# - Redis: localhost:6379
```

## API Examples

### Submit Application

```bash
curl -X POST http://localhost:8000/api/v1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-1024",
    "applicant_id": "USER-001",
    "applicant_first_name": "John",
    "applicant_last_name": "Doe",
    "applicant_email": "john@example.com",
    "applicant_phone": "+1-555-0100",
    "applicant_income": 8500,
    "credit_score": 720,
    "debt_to_income_ratio": 0.43,
    "employment_status": "FULL_TIME",
    "loan_amount": 50000,
    "loan_purpose": "Home Improvement"
  }'
```

### Get Workflow Status

```bash
curl http://localhost:8000/api/v1/status/applications/APP-1024/status
```

### Get Final Decision

```bash
curl http://localhost:8000/api/v1/decisions/applications/APP-1024/decision
```

## Key Design Patterns

### 1. **Typed Contracts**
Every agent has explicit Pydantic input/output schemas, enforcing data quality.

### 2. **Evidence Logging**
All decisions backed by immutable, timestamped evidence from each agent with source references.

### 3. **Durable State**
Workflow checkpoints enable recovery from failures without data loss.

### 4. **Idempotent Execution**
Tool calls use idempotency keys to prevent duplicate side effects during retries.

### 5. **Parallel Execution**
4 verification agents run concurrently, reducing end-to-end latency.

### 6. **Human-in-the-Loop**
High-risk cases automatically escalate to human reviewers instead of forcing confident but uncertain decisions.

### 7. **Observable Systems**
OpenTelemetry-compatible tracing correlates all related operations.

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit

# Integration tests
pytest tests/integration

# Evaluation suite (decision accuracy)
pytest evals/test_decision_accuracy.py

# With coverage
pytest --cov=. --cov-report=html
```

## Deployment Options

- **Local**: `uvicorn api.main:app --reload`
- **Docker Compose**: `docker-compose up --build`
- **Kubernetes**: See [docs/deployment/deployment.md](docs/deployment/deployment.md) for manifests
- **AWS ECS/RDS**: Detailed guide in deployment documentation

## Observability

- **Traces**: Jaeger at http://localhost:16686
- **Logs**: Structured JSON to stdout (filterable by application_id, workflow_id)
- **Metrics**: OpenTelemetry format (ready for Prometheus)

## What's Not Included (For Production)

The following are scaffolded but not fully implemented:

- **Storage/Database Layer**: Schemas defined, repository pattern ready
- **Real LLM Integration**: Agents use simulated logic, ready for LLM provider APIs
- **External Service Integration**: Tool gateway has templates for actual APIs
- **Authentication**: Basic structure, needs OAuth2/JWT implementation
- **Advanced Observability**: Metrics framework in place, needs Prometheus export

These are intentionally left as exercises to customize for your environment.

## Learning Objectives

This implementation teaches:

1. **Multi-agent system architecture** with clear separation of concerns
2. **Workflow orchestration** with state machines and durable execution
3. **Evidence-based decision making** with immutable audit trails
4. **Error handling** with retries, circuit breakers, and compensation
5. **Observability** with distributed tracing and structured logging
6. **Testing strategies** for agent systems (unit, integration, evaluation)
7. **Production readiness** patterns (health checks, graceful degradation)

## Resume Bullets

- Designed and implemented a durable multi-agent loan underwriting workflow with 7 specialized agents
- Built immutable evidence logging system with structured decision records
- Implemented workflow orchestration with parallel execution and 12-state state machine
- Created comprehensive test suite with golden dataset evaluation
- Containerized full-stack application with Docker Compose
- Documented production deployment patterns for Kubernetes and AWS

## Contributing

Pull requests welcome. Focus areas:

- Real LLM provider integration (OpenAI, Anthropic, etc.)
- Database persistence layer implementation
- Additional agent types
- Advanced observability (metrics, profiling)
- Security enhancements (authentication, rate limiting)
- Performance optimization

## License

MIT License

## Questions?

See [docs/](docs/) for architecture, deployment, and API documentation.
