"""
Tool schemas - external tool integration contracts.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ToolName(str, Enum):
    """Available tool names."""
    DOCUMENT_PARSER = "document_parser"
    PAYROLL_LOOKUP = "payroll_lookup"
    BANK_STATEMENT_API = "bank_statement_api"
    CREDIT_BUREAU = "credit_bureau"
    FRAUD_SERVICE = "fraud_service"
    POLICY_ENGINE = "policy_engine"
    BLACKLIST_CHECK = "blacklist_check"


class ToolInvocation(BaseModel):
    """Record of a tool invocation."""
    invocation_id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    workflow_id: str
    application_id: str
    
    tool_name: ToolName
    tool_version: str = Field(default="1.0")
    
    # Input
    input_parameters: Dict[str, Any]
    input_hash: str = Field(description="Hash of input for duplicate detection")
    
    # Idempotency
    idempotency_key: str = Field(description="Key for idempotent execution")
    
    # Status
    status: str = Field(default="PENDING")  # PENDING, RUNNING, SUCCESS, FAILURE, TIMEOUT
    
    # Output
    output: Optional[Dict[str, Any]] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    
    # Performance
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    latency_ms: Optional[int] = Field(default=None)
    
    # Retry
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)
    
    # Authentication
    auth_scope: str = Field(default="user", description="Auth scope used")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ToolResponse(BaseModel):
    """Response from a tool execution."""
    invocation_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: int


class PayrollLookupRequest(BaseModel):
    """Request to payroll lookup service."""
    applicant_id: str
    applicant_email: str
    months_back: int = Field(default=12)


class PayrollLookupResponse(BaseModel):
    """Response from payroll lookup service."""
    applicant_id: str
    found: bool
    monthly_salary: Optional[float] = None
    salary_history: Optional[List[Dict[str, Any]]] = None
    employer_name: Optional[str] = None
    employment_start_date: Optional[datetime] = None


class BankStatementRequest(BaseModel):
    """Request to bank statement API."""
    applicant_id: str
    months_back: int = Field(default=6)


class BankStatementResponse(BaseModel):
    """Response from bank statement API."""
    applicant_id: str
    found: bool
    average_monthly_deposit: Optional[float] = None
    account_age_months: Optional[int] = None
    transaction_summary: Optional[Dict[str, Any]] = None


class CreditBureauRequest(BaseModel):
    """Request to credit bureau service."""
    applicant_id: str
    applicant_ssn: Optional[str] = None


class CreditBureauResponse(BaseModel):
    """Response from credit bureau service."""
    applicant_id: str
    found: bool
    credit_score: Optional[int] = None
    payment_history: Optional[str] = None
    credit_history_months: Optional[int] = None
    accounts: Optional[List[Dict[str, Any]]] = None
    hard_inquiries: Optional[int] = None


class FraudServiceRequest(BaseModel):
    """Request to fraud detection service."""
    applicant_id: str
    applicant_email: str
    applicant_phone: str
    device_id: Optional[str] = None
    ip_address: Optional[str] = None


class FraudServiceResponse(BaseModel):
    """Response from fraud detection service."""
    applicant_id: str
    fraud_score: float = Field(ge=0, le=1)
    blacklisted: bool
    device_anomaly: bool
    velocity_check: bool
    fraud_flags: List[str] = Field(default_factory=list)


class PolicyEngineRequest(BaseModel):
    """Request to policy engine."""
    application_data: Dict[str, Any]
    policy_checks: List[str]


class PolicyEngineResponse(BaseModel):
    """Response from policy engine."""
    policy_passed: bool
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    policy_version: str


class DocumentParserRequest(BaseModel):
    """Request to document parser."""
    document_id: str
    document_type: str
    document_content: str


class DocumentParserResponse(BaseModel):
    """Response from document parser."""
    document_id: str
    extracted_fields: Dict[str, Any]
    confidence_scores: Dict[str, float]
    parsing_errors: List[str] = Field(default_factory=list)


class ToolRegistry(BaseModel):
    """Registry of allowed tools and their permissions."""
    tool_name: ToolName
    tool_version: str
    enabled: bool = Field(default=True)
    allowed_for_agents: List[str] = Field(description="Agent roles allowed to use")
    rate_limit: int = Field(default=100, description="Calls per minute")
    timeout_ms: int = Field(default=30000)
    requires_auth: bool = Field(default=True)
    requires_audit: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
