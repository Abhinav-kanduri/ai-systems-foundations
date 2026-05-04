# Quick Reference Guide

## Getting Started (5 minutes)

### 1. Local Development
```bash
git clone <repo>
cd reliable-multi-agent-loan-underwriting
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
# API: http://localhost:8000/docs
```

### 2. Docker Compose (Full Stack)
```bash
docker-compose up --build
# API: http://localhost:8000
# UI: http://localhost:8501
# Jaeger: http://localhost:16686
```

## Submitting Applications

```bash
curl -X POST http://localhost:8000/api/v1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-001",
    "applicant_id": "USER-001",
    "applicant_first_name": "John",
    "applicant_email": "john@example.com",
    "applicant_income": 8500,
    "credit_score": 720,
    "debt_to_income_ratio": 0.43,
    "loan_amount": 50000,
    "loan_purpose": "Home Improvement"
  }'
```

## Checking Status

```bash
# Workflow status
curl http://localhost:8000/api/v1/status/applications/APP-001/status

# Final decision
curl http://localhost:8000/api/v1/decisions/applications/APP-001/decision

# All evidence
curl http://localhost:8000/api/v1/status/workflows/{workflow_id}/evidence
```

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/unit/test_agents.py::test_document_intake_agent

# With coverage
pytest --cov=.

# Evaluation (accuracy)
pytest evals/test_decision_accuracy.py
```

## Code Organization

| Module | Purpose | Key Files |
|--------|---------|-----------|
| `agents/` | 7 specialized agents | `base.py`, `document_intake.py`, `income_verification.py`, ... |
| `schemas/` | Pydantic data models | `application.py`, `evidence.py`, `agents.py`, `decisions.py` |
| `orchestrator/` | Workflow orchestration | `states.py`, `workflow.py` |
| `api/` | FastAPI application | `main.py`, `routes/` |
| `storage/` | Database layer (scaffold) | `database.py`, `repositories.py` |
| `observability/` | Tracing & logging | `tracing.py`, `logging.py` |
| `tests/` | Test suite | `unit/`, `integration/`, `workflow/` |
| `evals/` | Evaluation tests | `test_decision_accuracy.py` |

## Workflow States

```
SUBMITTED 
  → DOCUMENT_INTAKE 
    → PARALLEL_VERIFICATION
      → INCOME_VERIFICATION
      → CREDIT_SCORING
      → FRAUD_DETECTION
      → COMPLIANCE_CHECK
    → RISK_ASSESSMENT
      → FINAL_DECISION
        → HUMAN_REVIEW (if needed)
          → COMPLETED
```

## Adding a New Agent

1. Create `agents/my_agent.py` inheriting from `BaseAgent`
2. Add schemas in `schemas/agents.py`
3. Register in `orchestrator/workflow.py`
4. Add tests in `tests/unit/test_agents.py`
5. Update documentation

Example:
```python
from agents.base import BaseAgent

class MyAgent(BaseAgent):
    async def execute(self, **kwargs):
        # Your logic
        return result
    
    def generate_evidence(self, output):
        # Evidence for audit trail
        return evidence
```

## Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `APP_ENV` | Environment | `local` |
| `DATABASE_URL` | Database connection | `sqlite:///./underwriting.db` |
| `REDIS_URL` | Cache | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | LLM provider key | Required for LLM models |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAX_AGENT_STEPS` | Max workflow steps | `12` |
| `HUMAN_REVIEW_CONFIDENCE_THRESHOLD` | Escalation threshold | `0.75` |

See `.env.example` for all options.

## Deployment

| Target | Command | Notes |
|--------|---------|-------|
| Local | `uvicorn api.main:app --reload` | Development only |
| Docker | `docker-compose up --build` | Full stack |
| Kubernetes | `kubectl apply -f k8s/` | Production recommended |
| AWS ECS | AWS console or CLI | See deployment guide |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | `lsof -i :8000` to find process |
| Import errors | Activate venv, reinstall: `pip install -r requirements.txt` |
| Database errors | Check `DATABASE_URL` in `.env` |
| Docker issues | `docker-compose down -v` to clean state |
| Tests failing | Run `pytest -v` to see details |

## Key Concepts

### Agents
Autonomous components handling specific concerns (income verification, fraud detection, etc.)

### Evidence
Immutable records of all decisions with sources, confidence, and reasoning

### Orchestration
Workflow engine managing agent sequencing, state, and failure recovery

### Idempotency
Safe retries using idempotency keys—same input always produces same output

### Human Review
Automatic escalation for high-risk cases to human judgment

## Monitoring

- **Logs**: Structured JSON to stdout
- **Traces**: View in Jaeger (http://localhost:16686)
- **Metrics**: OpenTelemetry format (ready for Prometheus)

Filter logs:
```bash
# By application
docker-compose logs api | grep APP-001

# By trace
docker-compose logs api | grep trace-abc-123
```

## Common Tasks

### View API Documentation
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)

### Reset Database
```bash
rm underwriting.db  # SQLite
# Or drop/recreate PostgreSQL database
```

### Restart Services
```bash
docker-compose down
docker-compose up
```

### View Traces
1. Open http://localhost:16686
2. Select service: "loan-underwriting-api"
3. Find by trace ID or application_id

### Check Health
```bash
curl http://localhost:8000/health
```

## Resources

- [README.md](README.md) - Main documentation
- [docs/architecture/architecture.md](docs/architecture/architecture.md) - System design
- [docs/deployment/deployment.md](docs/deployment/deployment.md) - Deployment guide
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Project overview
- [schemas/](schemas/) - Data model definitions
- [agents/](agents/) - Agent implementations

## Support

- Issues: GitHub Issues
- Questions: GitHub Discussions
- Email: engineering@example.com
