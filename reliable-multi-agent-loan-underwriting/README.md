# Reliable Multi-Agent Loan Underwriting System

**Author**: Abhinav Kanduri

## ⚠️ Important Note

This is a **mock/dummy implementation for learners** designed to demonstrate production-grade architectural patterns and best practices for multi-agent AI systems. The agent logic uses simulated workflows and is not intended for actual loan processing. Use this as a reference implementation to understand how to build reliable, observable, and governance-controlled agent systems.

## Project Overview

This is a **production-grade reference implementation** of a multi-agent AI workflow system for loan underwriting. It demonstrates how to engineer reliable, observable, and governance-controlled agent systems in Python.

## Quick Start

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git

### Local Setup (Development)

> **Note**: This is a learning/reference implementation with simulated agent logic. See [PROBLEM_STATEMENT.md](PROBLEM_STATEMENT.md) for the educational context.

```bash
# Clone repository
git clone <repository-url>
cd reliable-multi-agent-loan-underwriting

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Update .env with your configuration

# Run migrations (if using PostgreSQL)
alembic upgrade head

# Start API server
uvicorn api.main:app --reload

# API will be available at http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

### Docker Compose (Full Stack)

```bash
# Build and start all services
docker-compose up --build

# API: http://localhost:8000
# UI Dashboard: http://localhost:8501
# Jaeger Traces: http://localhost:16686
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

## Project Structure

```
reliable-multi-agent-loan-underwriting/
├── api/                              # FastAPI application
│   ├── main.py                       # App initialization
│   └── routes/                       # API endpoints
│       ├── applications.py           # Submission and management
│       ├── status.py                 # Workflow status
│       ├── decisions.py              # Decision retrieval
│       └── human_review.py           # Human review workflow
├── agents/                           # Multi-agent system
│   ├── base.py                       # Base agent class
│   ├── document_intake.py            # Document parsing
│   ├── income_verification.py        # Income verification
│   ├── credit_scoring.py             # Credit assessment
│   ├── fraud_detection.py            # Fraud detection
│   ├── compliance.py                 # Compliance checking
│   ├── risk_assessment.py            # Risk aggregation
│   └── final_approval.py             # Approval decision
├── orchestrator/                     # Workflow orchestration
│   ├── states.py                     # State machine definition
│   └── workflow.py                   # Orchestrator engine
├── schemas/                          # Pydantic models
│   ├── application.py                # Loan application schemas
│   ├── evidence.py                   # Evidence logging
│   ├── agents.py                     # Agent I/O contracts
│   ├── decisions.py                  # Decision records
│   ├── workflow.py                   # Workflow state
│   └── tools.py                      # Tool integration
├── storage/                          # Database and persistence
│   ├── database.py                   # Database setup
│   ├── repositories.py               # Data access layer
│   └── migrations/                   # Database migrations
├── observability/                    # Tracing and monitoring
│   ├── tracing.py                    # OpenTelemetry setup
│   └── logging.py                    # Structured logging
├── tests/                            # Test suite
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   └── workflow/                     # End-to-end workflow tests
├── evals/                            # Evaluation suite
│   ├── golden_dataset.json           # Test cases
│   ├── test_decision_accuracy.py     # Accuracy tests
│   └── test_failure_recovery.py      # Reliability tests
├── docs/                             # Documentation
│   ├── architecture.md               # Architecture guide
│   ├── deployment.md                 # Deployment guide
│   └── api.md                        # API reference
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Docker image
├── pyproject.toml                    # Project metadata
├── requirements.txt                  # Dependencies
└── .env.example                      # Environment template
```

## Key Features

### 1. **Multi-Agent Architecture**
- 7 specialized agents for different underwriting concerns
- Clear separation of responsibilities
- Typed input/output contracts via Pydantic

### 2. **Durable Workflow State**
- Checkpoints for recovery after failures
- Optimistic concurrency control
- State versioning and snapshots

### 3. **Immutable Evidence Logging**
- All evidence recorded chronologically
- Source references for traceability
- Confidence scores with each decision

### 4. **Idempotent Execution**
- Tool invocations use idempotency keys
- Duplicate detection via input hashing
- Safe retries without side effects

### 5. **Observability**
- OpenTelemetry-style tracing
- Span recording for agents, tools, and transitions
- Structured JSON logging
- Distributed trace correlation

### 6. **Governance Controls**
- Tool gateway with policy enforcement
- Rate limiting and timeout controls
- Human approval gates for high-risk cases
- Audit logging of all actions

### 7. **Error Handling & Recovery**
- Bounded retries with exponential backoff
- Circuit breaker for failing dependencies
- Compensation for partial side effects
- Graceful degradation

## API Endpoints

### Submit Application
```http
POST /api/v1/applications
Content-Type: application/json

{
  "application_id": "APP-1024",
  "applicant_id": "USER-7788",
  "applicant_first_name": "John",
  "applicant_last_name": "Doe",
  "applicant_email": "john@example.com",
  "applicant_phone": "+1-555-0100",
  "applicant_income": 8500,
  "credit_score": 720,
  "debt_to_income_ratio": 0.43,
  "employment_status": "FULL_TIME",
  "employment_length_months": 36,
  "loan_amount": 50000,
  "loan_purpose": "Home Improvement",
  "fraud_signals": {
    "device_mismatch": false,
    "identity_mismatch": false
  },
  "documents": ["PAYSTUB", "BANK_STATEMENT", "ID_PROOF"]
}
```

### Get Application Status
```http
GET /api/v1/status/applications/{application_id}/status
```

### Get Final Decision
```http
GET /api/v1/decisions/applications/{application_id}/decision
```

### Get Workflow Evidence
```http
GET /api/v1/status/workflows/{workflow_id}/evidence
```

### Submit Human Review
```http
POST /api/v1/human-review/applications/{application_id}/review
Content-Type: application/json

{
  "reviewer_id": "reviewer-001",
  "decision": "APPROVED_WITH_CONDITIONS",
  "override_reason": "Verified income manually with employer records."
}
```

## Configuration

### Environment Variables

```bash
# Application
APP_ENV=local                           # Environment: local, staging, production
DEBUG=true                              # Enable debug mode

# API Server
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./underwriting.db

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM Configuration
OPENAI_API_KEY=your-key-here
MODEL_NAME=gpt-4-turbo-preview

# Workflow
MAX_AGENT_STEPS=12
MAX_TOOL_RETRIES=3
HUMAN_REVIEW_CONFIDENCE_THRESHOLD=0.75

# Observability
TRACE_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
LOG_LEVEL=INFO
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Unit Tests
```bash
pytest tests/unit
```

### Run Integration Tests
```bash
pytest tests/integration
```

### Run End-to-End Workflow Tests
```bash
pytest tests/workflow
```

### Run Evaluation Suite
```bash
pytest evals/
```

### Generate Coverage Report
```bash
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

## Development

### Code Style
```bash
# Format code
black .

# Lint code
ruff check . --fix

# Type checking
mypy .
```

### Adding a New Agent

1. Create agent class inheriting from `BaseAgent`
2. Implement `execute()` method with agent logic
3. Implement `generate_evidence()` for tracing
4. Add Pydantic input/output schemas
5. Register in `WorkflowOrchestrator`
6. Add tests in `tests/unit/agents/`

Example:

```python
from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="MyAgent",
            agent_version="1.0.0"
        )
    
    async def execute(self, **kwargs):
        # Implementation
        result = {}
        return result
    
    def generate_evidence(self, agent_output):
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.CUSTOM,
            description="...",
            key_findings={},
            confidence=0.95,
            source_refs=[]
        )
```

## Deployment

### Local Development
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Compose (Full Stack)
```bash
docker-compose up --build
```

### Kubernetes (Production)
See [deployment.md](docs/deployment.md) for Kubernetes manifests and best practices.

### Production Checklist
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up Redis cluster for caching and state
- [ ] Configure OpenTelemetry for distributed tracing
- [ ] Enable HTTPS/TLS
- [ ] Configure authentication and API keys
- [ ] Set up log aggregation
- [ ] Configure monitoring and alerting
- [ ] Run security audit
- [ ] Load test the system
- [ ] Create disaster recovery plan

## Monitoring & Observability

### Traces
- View distributed traces in Jaeger: http://localhost:16686
- Filter by application_id, workflow_id, or trace_id
- Examine agent execution times and dependencies

### Logs
- Structured JSON logs to stdout
- Log level configurable via LOG_LEVEL
- Searchable in centralized log aggregation (ELK, Datadog, etc.)

### Metrics
- OpenTelemetry metrics (experimental)
- Custom metrics for decision accuracy and latency
- Export to Prometheus for Grafana dashboards

## Troubleshooting

### API won't start
```bash
# Check port is available
lsof -i :8000

# Check environment variables
env | grep APP_

# Review logs
docker-compose logs api
```

### Workflow hangs
- Check agent logs for exceptions
- Verify external service connectivity (credit bureau, payroll, etc.)
- Review workflow state: `GET /api/v1/status/workflows/{id}/trace`

### Database issues
```bash
# Check database connection
psql postgresql://user:password@localhost:5432/underwriting -c "SELECT 1"

# Run migrations
alembic upgrade head

# Reset database (development only)
rm underwriting.db
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Implement changes with tests
4. Format and lint: `black . && ruff check . --fix && mypy .`
5. Run tests: `pytest`
6. Commit: `git commit -am "Add feature"`
7. Push: `git push origin feature/my-feature`
8. Create pull request

## License

MIT License - See LICENSE file

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report a bug](../../issues)
- Discussions: [Ask a question](../../discussions)
- Email: abhinav.kanduri01@gmail.com
