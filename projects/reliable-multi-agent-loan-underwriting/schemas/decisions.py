"""
Decision schemas - final underwriting decision and related types.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ApprovalDecision(str, Enum):
    """Final approval decision."""
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    APPROVED_WITH_CONDITIONS = "APPROVED_WITH_CONDITIONS"


class RiskLevel(str, Enum):
    """Risk level classification."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    MEDIUM_HIGH = "MEDIUM_HIGH"
    HIGH = "HIGH"


class UnderwritingDecision(BaseModel):
    """Final underwriting decision record."""
    decision_id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    application_id: str = Field(..., description="Associated application")
    
    # Decision
    decision: ApprovalDecision = Field(..., description="Final decision")
    risk_level: RiskLevel = Field(..., description="Risk classification")
    approval_confidence: float = Field(ge=0, le=1, description="Confidence in decision")
    
    # Evidence and reasoning
    reason_codes: List[str] = Field(default_factory=list, description="Structured reason codes")
    detailed_explanation: str = Field(..., description="Human-readable explanation")
    
    # Agent evidence summary
    agent_evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence from each agent")
    
    # Human review
    human_review_required: bool = Field(default=False)
    escalation_reason: Optional[str] = Field(default=None)
    reviewer_notes: Optional[str] = Field(default=None)
    reviewer_id: Optional[str] = Field(default=None)
    reviewed_at: Optional[datetime] = Field(default=None)
    
    # Traceability
    trace_id: str = Field(..., description="Trace ID for complete workflow trace")
    workflow_id: str = Field(..., description="Associated workflow ID")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Audit
    audit_status: str = Field(default="PENDING", description="PENDING, COMPLETE, REVIEWED")
    audit_timestamp: Optional[datetime] = Field(default=None)


class HumanReviewRequest(BaseModel):
    """Request for human review of an application."""
    application_id: str
    workflow_id: str
    decision_id: str
    escalation_reason: str
    supporting_evidence: Dict[str, Any]
    priority: str = Field(default="NORMAL")  # LOW, NORMAL, HIGH, URGENT
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HumanReviewResponse(BaseModel):
    """Human reviewer's decision response."""
    review_id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    application_id: str
    decision_id: str
    reviewer_id: str
    
    decision: ApprovalDecision
    override_reason: str
    supporting_notes: Optional[str] = None
    
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Approval if conditions
    conditions: List[str] = Field(default_factory=list)


class DecisionSummary(BaseModel):
    """Summary of decision for API responses."""
    application_id: str
    decision: ApprovalDecision
    risk_level: RiskLevel
    reason_codes: List[str]
    trace_id: str
    human_review_required: bool
    approval_confidence: float
    created_at: datetime


class AuditableDecisionLog(BaseModel):
    """Audit-ready decision log entry."""
    decision_id: str
    application_id: str
    decision: ApprovalDecision
    risk_level: RiskLevel
    
    # All evidence
    all_evidence: Dict[str, Any]
    
    # Model and prompt versions
    model_name: str
    model_version: str
    prompt_version: str
    
    # Execution details
    workflow_id: str
    trace_id: str
    agent_versions: Dict[str, str]
    
    # Human review if applicable
    human_reviewed: bool
    reviewer_id: Optional[str] = None
    override_decision: Optional[ApprovalDecision] = None
    
    # Timestamps
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    
    # Compliance
    compliant_with_policies: bool
    policy_version: str
    regulatory_notes: Optional[str] = None
