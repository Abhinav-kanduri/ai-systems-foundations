"""
Workflow schemas - orchestration and state management.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    SUBMITTED = "SUBMITTED"
    DOCUMENT_INTAKE = "DOCUMENT_INTAKE"
    PARALLEL_VERIFICATION = "PARALLEL_VERIFICATION"
    INCOME_VERIFICATION = "INCOME_VERIFICATION"
    CREDIT_SCORING = "CREDIT_SCORING"
    FRAUD_DETECTION = "FRAUD_DETECTION"
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    FINAL_DECISION = "FINAL_DECISION"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WorkflowState(BaseModel):
    """Current state of a workflow."""
    workflow_id: str = Field(..., description="Unique workflow ID")
    application_id: str = Field(..., description="Associated application")
    
    current_step: WorkflowStatus = Field(..., description="Current workflow step")
    status: str = Field(default="RUNNING", description="RUNNING, COMPLETED, FAILED")
    
    # State version for optimistic concurrency
    state_version: int = Field(default=0, description="State version for optimistic locking")
    
    # Completed agents
    completed_agents: List[str] = Field(default_factory=list)
    pending_agents: List[str] = Field(default_factory=list)
    failed_agents: List[str] = Field(default_factory=list)
    
    # Retries and errors
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)
    last_error: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Context data
    context: Dict[str, Any] = Field(default_factory=dict, description="Workflow context data")
    
    # Idempotency
    idempotency_key: Optional[str] = Field(default=None, description="For replay protection")


class WorkflowCheckpoint(BaseModel):
    """Checkpoint for durable workflow execution."""
    checkpoint_id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    workflow_id: str
    application_id: str
    
    current_step: WorkflowStatus
    state_snapshot: Dict[str, Any] = Field(description="Serialized workflow state")
    
    completed_agents_output: Dict[str, Any] = Field(default_factory=dict)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    checkpoint_hash: str = Field(description="SHA256 hash of state for integrity check")


class WorkflowTransition(BaseModel):
    """Record of a workflow state transition."""
    transition_id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    workflow_id: str
    application_id: str
    
    from_step: WorkflowStatus
    to_step: WorkflowStatus
    
    triggered_by: str = Field(description="Agent or system that triggered transition")
    trigger_reason: Optional[str] = Field(default=None)
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RetryPolicy(BaseModel):
    """Retry policy for workflow and agent execution."""
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    initial_delay_ms: int = Field(default=1000, description="Initial backoff delay")
    max_delay_ms: int = Field(default=30000, description="Maximum backoff delay")
    backoff_factor: float = Field(default=2.0, description="Exponential backoff factor")
    
    # Circuit breaker
    circuit_breaker_threshold: int = Field(default=5, description="Failure threshold")
    circuit_breaker_reset_ms: int = Field(default=60000, description="Reset timeout")
    
    # Timeout
    operation_timeout_ms: int = Field(default=30000, description="Operation timeout")


class WorkflowMetrics(BaseModel):
    """Metrics for workflow execution."""
    workflow_id: str
    application_id: str
    
    total_duration_ms: int
    agent_execution_times: Dict[str, int] = Field(default_factory=dict)
    
    total_retries: int = Field(default=0)
    tool_calls_count: int = Field(default=0)
    tool_call_failures: int = Field(default=0)
    
    human_review_required: bool = Field(default=False)
    human_review_time_ms: Optional[int] = Field(default=None)
    
    decision_confidence: float = Field(ge=0, le=1)
    
    # Cost tracking
    llm_tokens_used: int = Field(default=0)
    estimated_cost_usd: float = Field(default=0.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
