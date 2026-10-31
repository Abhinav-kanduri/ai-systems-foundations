"""
Agent schemas - defines contracts for agent inputs, outputs, and states.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    """Agent roles in the workflow."""
    DOCUMENT_INTAKE = "DOCUMENT_INTAKE"
    INCOME_VERIFICATION = "INCOME_VERIFICATION"
    CREDIT_SCORING = "CREDIT_SCORING"
    FRAUD_DETECTION = "FRAUD_DETECTION"
    COMPLIANCE = "COMPLIANCE"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    FINAL_APPROVAL = "FINAL_APPROVAL"


class AgentStatus(str, Enum):
    """Agent execution status."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"


class DocumentIntakeInput(BaseModel):
    """Input for Document Intake Agent."""
    application_id: str
    applicant_id: str
    document_ids: List[str] = Field(default_factory=list)
    documents_content: Optional[Dict[str, str]] = Field(default=None)


class DocumentIntakeOutput(BaseModel):
    """Output from Document Intake Agent."""
    application_id: str
    extracted_fields: Dict[str, Any] = Field(description="Extracted information")
    missing_documents: List[str] = Field(default_factory=list)
    document_quality: Dict[str, float] = Field(description="Quality scores per document")
    processing_errors: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    requires_manual_review: bool = Field(default=False)


class IncomeVerificationInput(BaseModel):
    """Input for Income Verification Agent."""
    application_id: str
    applicant_id: str
    stated_income: float
    employment_status: str
    employment_length_months: int
    paystub_data: Optional[Dict[str, Any]] = None
    bank_statement_data: Optional[Dict[str, Any]] = None


class IncomeVerificationOutput(BaseModel):
    """Output from Income Verification Agent."""
    application_id: str
    verification_status: str  # MATCH, MISMATCH, INSUFFICIENT_EVIDENCE
    stated_income: float
    verified_income: float
    variance_percentage: float
    verification_source: List[str]
    confidence: float = Field(ge=0, le=1)
    reason_codes: List[str] = Field(default_factory=list)
    requires_escalation: bool = Field(default=False)


class CreditScoringInput(BaseModel):
    """Input for Credit Scoring Agent."""
    application_id: str
    applicant_id: str
    credit_score: Optional[int] = None
    loan_amount: float
    loan_purpose: str


class CreditScoringOutput(BaseModel):
    """Output from Credit Scoring Agent."""
    application_id: str
    credit_score: int
    credit_risk_level: str  # LOW, MEDIUM, HIGH
    risk_factors: List[str] = Field(default_factory=list)
    credit_history_length_months: int
    confidence: float = Field(ge=0, le=1)
    reason_codes: List[str] = Field(default_factory=list)


class FraudDetectionInput(BaseModel):
    """Input for Fraud Detection Agent."""
    application_id: str
    applicant_id: str
    applicant_email: str
    applicant_phone: str
    device_info: Optional[Dict[str, Any]] = None
    behavioral_data: Optional[Dict[str, Any]] = None
    fraud_signals: Optional[Dict[str, bool]] = None


class FraudDetectionOutput(BaseModel):
    """Output from Fraud Detection Agent."""
    application_id: str
    fraud_risk_score: float = Field(ge=0, le=1)
    fraud_detected: bool
    fraud_flags: List[str] = Field(default_factory=list)
    blacklist_match: bool = Field(default=False)
    risk_level: str  # LOW, MEDIUM, HIGH
    confidence: float = Field(ge=0, le=1)
    reason_codes: List[str] = Field(default_factory=list)
    requires_escalation: bool = Field(default=False)


class ComplianceCheckInput(BaseModel):
    """Input for Compliance Agent."""
    application_id: str
    applicant_first_name: str
    applicant_last_name: str
    applicant_email: str
    loan_amount: float


class ComplianceCheckOutput(BaseModel):
    """Output from Compliance Agent."""
    application_id: str
    sanction_check_passed: bool
    aml_check_passed: bool
    regulatory_compliance: bool
    policy_violations: List[str] = Field(default_factory=list)
    regulatory_notes: Optional[str] = None
    confidence: float = Field(ge=0, le=1)
    requires_manual_review: bool = Field(default=False)


class RiskAssessmentInput(BaseModel):
    """Input for Risk Assessment Agent."""
    application_id: str
    applicant_income: float
    loan_amount: float
    debt_to_income_ratio: float
    credit_score: int
    employment_status: str
    # Evidence from other agents
    income_verification_result: Optional[Dict[str, Any]] = None
    credit_scoring_result: Optional[Dict[str, Any]] = None
    fraud_detection_result: Optional[Dict[str, Any]] = None
    compliance_result: Optional[Dict[str, Any]] = None


class RiskAssessmentOutput(BaseModel):
    """Output from Risk Assessment Agent."""
    application_id: str
    overall_risk_level: str  # LOW, MEDIUM, MEDIUM_HIGH, HIGH
    risk_score: float = Field(ge=0, le=1)
    risk_factors: Dict[str, float] = Field(description="Weighted risk factors")
    risk_summary: str
    confidence: float = Field(ge=0, le=1)
    requires_escalation: bool = Field(default=False)


class FinalApprovalInput(BaseModel):
    """Input for Final Approval Agent."""
    application_id: str
    applicant_income: float
    loan_amount: float
    risk_assessment_result: Dict[str, Any]
    # All evidence collected
    all_evidence: Optional[Dict[str, Any]] = None


class FinalApprovalOutput(BaseModel):
    """Output from Final Approval Agent."""
    application_id: str
    decision: str  # APPROVED, REJECTED, ESCALATE_TO_HUMAN
    risk_level: str
    reason_codes: List[str] = Field(default_factory=list)
    approval_confidence: float = Field(ge=0, le=1)
    human_review_required: bool = Field(default=False)
    escalation_reason: Optional[str] = None


class AgentStateSnapshot(BaseModel):
    """Snapshot of agent state during workflow execution."""
    agent_role: AgentRole
    agent_name: str
    agent_version: str
    status: AgentStatus
    
    input_schema: Optional[str] = Field(default=None)
    output_schema: Optional[str] = Field(default=None)
    
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    
    retry_count: int = Field(default=0)
    error_message: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
