# Architecture Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  (Web UI, Mobile, Third-party Integrations)                 │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│                  API Gateway Layer                           │
│  ├─ Request Validation                                       │
│  ├─ Authentication & Authorization                           │
│  ├─ Rate Limiting                                            │
│  └─ Request Correlation (Trace ID)                           │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│              Business Logic Layer                            │
│  ├─ Application Submission Handler                           │
│  ├─ Workflow Orchestrator                                    │
│  ├─ State Machine Management                                 │
│  └─ Human Review Workflow                                    │
└────────────────────────────────────────────────────────────┘
         │                     │                      │
         ▼                     ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Agent Layer     │  │  Evidence Log    │  │  Tool Gateway    │
│                  │  │                  │  │                  │
│ ├─ Document     │  │ ├─ Immutable    │  │ ├─ Document      │
│ │   Intake      │  │ │   Append-only │  │ │   Parser        │
│ │                │  │ │   Log         │  │ │                  │
│ ├─ Income       │  │ ├─ Evidence     │  │ ├─ Payroll       │
│ │   Verification│  │ │   Items       │  │ │   Lookup        │
│ │                │  │ ├─ Confidence  │  │ ├─ Credit Bureau │
│ ├─ Credit       │  │ │   Scores      │  │ │                  │
│ │   Scoring     │  │ └─ Source Refs  │  │ ├─ Fraud Service │
│ │                │  │                  │  │ └─ Policy Engine│
│ ├─ Fraud        │  │ (Persistent     │  │                  │
│ │   Detection   │  │  Storage)        │  │ (External APIs) │
│ ├─ Compliance   │  └──────────────────┘  └──────────────────┘
│ ├─ Risk         │
│ │   Assessment  │
│ └─ Final        │
│    Approval     │
└──────────────────┘

         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│              Data & State Layer                              │
│                                                               │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Workflow State  │    │  Checkpoints     │               │
│  │  ├─ Current Step │    │  ├─ Snapshots    │               │
│  │  ├─ History      │    │  ├─ Hashes       │               │
│  │  └─ Context      │    │  └─ Recovery     │               │
│  └──────────────────┘    └──────────────────┘               │
│                                                               │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  PostgreSQL      │    │  Redis Cache     │               │
│  │  (Persistent)    │    │  (Ephemeral)     │               │
│  └──────────────────┘    └──────────────────┘               │
└──────────────────────────────────────────────────────────────┘

         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│           Observability & Monitoring Layer                   │
│                                                               │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Tracing         │    │  Logging         │               │
│  │  ├─ Distributed  │    │  ├─ Structured  │               │
│  │  │   Traces      │    │  │   JSON       │               │
│  │  ├─ OpenTel.     │    │  ├─ Levels      │               │
│  │  │   Spans       │    │  └─ Correlation │               │
│  │  └─ Jaeger       │    │                  │               │
│  └──────────────────┘    └──────────────────┘               │
│                                                               │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Metrics         │    │  Audit Log       │               │
│  │  ├─ Latency      │    │  ├─ All Actions  │               │
│  │  ├─ Throughput   │    │  ├─ Actor Info   │               │
│  │  └─ Errors       │    │  └─ Compliance   │               │
│  └──────────────────┘    └──────────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

## Workflow State Machine

```
START
  │
  ├─> SUBMITTED
  │     │
  │     └─> DOCUMENT_INTAKE (1 agent)
  │           │
  │           └─> PARALLEL_VERIFICATION (5 agents run concurrently)
  │                 ├─> INCOME_VERIFICATION
  │                 ├─> CREDIT_SCORING
  │                 ├─> FRAUD_DETECTION
  │                 └─> COMPLIANCE_CHECK
  │                       │
  │                       └─> RISK_ASSESSMENT (aggregates all evidence)
  │                             │
  │                             └─> FINAL_DECISION
  │                                   │
  │                                   ├─ Decision = APPROVED
  │                                   │   └─> COMPLETED
  │                                   │
  │                                   ├─ Decision = REJECTED
  │                                   │   └─> COMPLETED
  │                                   │
  │                                   └─ Decision = ESCALATE_TO_HUMAN
  │                                       └─> HUMAN_REVIEW
  │                                             │
  │                                             ├─> APPROVED (by human)
  │                                             │   └─> COMPLETED
  │                                             │
  │                                             └─> REJECTED (by human)
  │                                                 └─> COMPLETED
  │
  └─ ERROR/TIMEOUT
        └─> FAILED

```

## Agent Responsibility Matrix

| Agent | Input | Output | Dependencies | Tools | Evidence Type |
|-------|-------|--------|--------------|-------|-----------------|
| Document Intake | Application + Documents | Extracted Fields | None | Document Parser | DOCUMENT_EXTRACTION |
| Income Verification | Applicant + Income Data | Verification Status | None | Payroll API, Bank API | INCOME_VERIFICATION |
| Credit Scoring | Applicant + Loan Info | Credit Risk | None | Credit Bureau | CREDIT_CHECK |
| Fraud Detection | Applicant + Device Info | Fraud Score | None | Fraud Service | FRAUD_ASSESSMENT |
| Compliance | Applicant + Loan Amount | Compliance Status | None | Policy Engine | COMPLIANCE_CHECK |
| Risk Assessment | All Upstream Results | Overall Risk | All agents | None | RISK_CALCULATION |
| Final Approval | Risk Assessment | Decision | Risk Assessment | None | APPROVAL_DECISION |

## Data Flow

### Application Submission → Decision

1. **Submission**
   - Client submits `LoanApplicationRequest`
   - API validates schema and creates `LoanApplication` record
   - Workflow orchestrator initialized with unique `workflow_id`
   - Background task starts workflow execution

2. **Document Intake**
   - Agent parses provided documents
   - Extracts relevant fields
   - Records extraction confidence
   - Flags missing documents

3. **Parallel Verification** (4 agents run concurrently)
   - **Income**: Compare stated vs. verified income
   - **Credit**: Fetch and score credit history
   - **Fraud**: Check for fraud signals and anomalies
   - **Compliance**: Verify regulatory requirements

4. **Risk Aggregation**
   - Risk Assessment Agent collects all evidence
   - Computes weighted risk factors
   - Assigns overall risk level
   - Generates risk summary

5. **Final Decision**
   - Final Approval Agent recommends: APPROVED, REJECTED, or ESCALATE
   - If escalation needed, routes to human review queue
   - If auto-approved/rejected, completes workflow

6. **Human Review** (if needed)
   - Application enters review queue
   - Human reviewer examines evidence
   - Reviewer makes final decision (approve, reject, approve with conditions)
   - Updates `UnderwritingDecision` with reviewer ID and override notes

### Evidence Flow

```
Agent Execution
  │
  ├─> Generate Evidence Item
  │   ├─ Agent name & version
  │   ├─ Evidence type (from EvidenceType enum)
  │   ├─ Key findings (structured data)
  │   ├─ Confidence score
  │   └─ Source references
  │
  ├─> Add to Immutable Evidence Log
  │   ├─ Append-only (no updates)
  │   ├─ Timestamp each item
  │   ├─ Track source document references
  │   └─ Preserve exact output for audit
  │
  └─> Include in Final Decision Record
      ├─ All evidence items referenced
      ├─ Decision confidence calculated from evidence
      ├─ Reason codes linked to evidence
      └─ Trace ID correlates all related records
```

## Reliability Patterns

### Checkpointing
- Created after each agent completes
- Stores workflow state snapshot
- Includes all completed agent outputs
- Enables recovery to last checkpoint on failure

### Idempotency
- Tool calls include idempotency key
- Input parameters hashed for duplicate detection
- Same input yields same result on retry
- Prevents duplicate transactions (e.g., multiple charges)

### Retry Logic
```
for attempt in range(max_retries):
    try:
        result = execute_agent()
        return result
    except TemporaryError:
        wait(backoff_delay(attempt))
    except PermanentError:
        raise
    except Timeout:
        if attempt < max_retries - 1:
            wait(backoff_delay(attempt))
        else:
            raise
```

### Circuit Breaker
- Track consecutive failures for external service
- After N failures, stop attempting for M seconds
- Fail fast instead of timing out
- Example: Credit bureau fails 5x → open circuit for 60s

### Compensation
- On workflow failure after side effects:
  - Rollback database changes
  - Cancel pending tool calls
  - Log compensation action for audit
  - Retry from last checkpoint

## Concurrency Model

### Parallel Agent Execution
```python
# During PARALLEL_VERIFICATION step:
tasks = [
    income_agent.run(data),
    credit_agent.run(data),
    fraud_agent.run(data),
    compliance_agent.run(data)
]

results = await asyncio.gather(*tasks)  # All run concurrently

# Continue only after all complete (implicit barrier)
risk_agent.run(results)
```

### Thread Safety
- Each workflow has isolated state
- No shared mutable state between workflows
- Redis for distributed locks (if needed)
- Database transactions for consistency

## Security & Governance

### Tool Access Control
```
Tool Authorization:
  ├─ Tool Registry defines allowed agents
  ├─ Rate limits per agent per tool
  ├─ Timeout enforcement
  ├─ Input validation
  ├─ Output sanitization
  └─ Audit logging
```

### Human Escalation
```
Automatic Escalation Triggers:
  ├─ Confidence < threshold
  ├─ Risk level = HIGH
  ├─ Conflicting evidence
  ├─ Policy violation
  └─ Tool timeout/failure
```

### Audit Trail
```
Audit Log Records:
  ├─ Actor (agent, human, system)
  ├─ Action (decision, escalation, override)
  ├─ Resource (application ID)
  ├─ Timestamp
  ├─ Trace ID (for correlation)
  └─ Outcome
```

## Scalability Considerations

### Horizontal Scaling
- **Stateless API**: Multiple instances behind load balancer
- **Workflow State**: Stored in PostgreSQL (single source of truth)
- **Cache**: Redis cluster for distributed session state
- **Tasks**: Message queue (e.g., Celery) for async execution

### Performance Optimization
- Database indexes on `application_id`, `workflow_id`, `created_at`
- Cached agent responses (Redis) with TTL
- Parallel agent execution reduces latency
- Async I/O for external service calls

### Resource Management
- Memory limits per container
- CPU limits per workflow
- Max workflow duration timeout
- Connection pool sizing for database

## High Availability

### Recovery Points
1. **Application submission** → database persistent
2. **Workflow checkpoint** → database persistent
3. **Agent output** → memory + evidence log
4. **Final decision** → database persistent + Redis cache

### Failure Scenarios

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Agent timeout | Timer expires | Retry with backoff |
| External API down | HTTP 5xx or timeout | Circuit breaker + fallback |
| Database unavailable | Connection error | Queued in Redis, replay on recovery |
| Partial workflow failure | Agent exception | Rollback and retry from checkpoint |
| Missing evidence | Validation error | Escalate to human review |

## Monitoring Points

### Critical Metrics
- **Latency**: End-to-end workflow duration
- **Throughput**: Applications processed per minute
- **Error rate**: % of workflows failing
- **Decision distribution**: % approved/rejected/escalated
- **Human review rate**: % escalated to humans

### Alert Triggers
- Workflow latency > 5 minutes
- Error rate > 5%
- Human review queue > 100 items
- External service latency > 2 seconds
- Database connection pool exhausted

## Cost Optimization

- Cache agent outputs to reduce recomputation
- Batch operations to external APIs
- Use cheaper models for low-confidence cases
- Parallelize to reduce wall-clock time
- Minimize LLM token usage with structured outputs
