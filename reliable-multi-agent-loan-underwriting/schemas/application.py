"""
Application schema - represents a loan application submission.
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class EmploymentStatus(str, Enum):
    """Employment status enum."""
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    RETIRED = "RETIRED"


class DocumentType(str, Enum):
    """Document types."""
    PAYSTUB = "PAYSTUB"
    BANK_STATEMENT = "BANK_STATEMENT"
    ID_PROOF = "ID_PROOF"
    TAX_RETURN = "TAX_RETURN"
    EMPLOYMENT_LETTER = "EMPLOYMENT_LETTER"
    PROOF_OF_RESIDENCE = "PROOF_OF_RESIDENCE"


class FraudSignals(BaseModel):
    """Fraud signal indicators."""
    device_mismatch: bool = Field(default=False, description="Device location anomaly")
    identity_mismatch: bool = Field(default=False, description="Identity verification mismatch")
    velocity_check: bool = Field(default=False, description="Unusual submission velocity")
    duplicate_application: bool = Field(default=False, description="Potential duplicate submission")


class LoanApplicationRequest(BaseModel):
    """Loan application submission request."""
    application_id: str = Field(..., description="Unique application identifier")
    applicant_id: str = Field(..., description="Applicant identifier")
    applicant_first_name: str = Field(..., description="First name")
    applicant_last_name: str = Field(..., description="Last name")
    applicant_email: str = Field(..., description="Email address")
    applicant_phone: str = Field(..., description="Phone number")
    
    # Financial information
    applicant_income: float = Field(..., ge=0, description="Monthly income in USD")
    credit_score: Optional[int] = Field(default=None, ge=300, le=850, description="Credit score")
    debt_to_income_ratio: float = Field(..., ge=0, le=1, description="DTI ratio")
    employment_status: EmploymentStatus = Field(..., description="Employment status")
    employment_length_months: int = Field(default=0, description="Months employed")
    
    # Loan information
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in USD")
    loan_purpose: str = Field(..., description="Purpose of loan")
    
    # Fraud and documents
    fraud_signals: FraudSignals = Field(default_factory=FraudSignals, description="Fraud signal indicators")
    documents: List[DocumentType] = Field(default_factory=list, description="Submitted document types")
    
    # Additional context
    tenant_id: Optional[str] = Field(default=None, description="Tenant/organization ID")
    additional_notes: Optional[str] = Field(default=None, description="Additional applicant notes")


class LoanApplication(LoanApplicationRequest):
    """Full loan application record with metadata."""
    submitted_at: datetime = Field(default_factory=datetime.utcnow, description="Submission timestamp")
    status: str = Field(default="SUBMITTED", description="Current application status")
    workflow_id: Optional[str] = Field(default=None, description="Associated workflow ID")
