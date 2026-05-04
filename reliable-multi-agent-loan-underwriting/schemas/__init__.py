"""
Schemas package initialization.
"""

from schemas.application import (
    LoanApplication,
    LoanApplicationRequest,
    EmploymentStatus,
    DocumentType,
    FraudSignals
)

from schemas.evidence import (
    EvidenceItem,
    EvidenceLog,
    EvidenceType,
    VerificationStatus
)

from schemas.agents import (
    DocumentIntakeInput,
    DocumentIntakeOutput,
    IncomeVerificationInput,
    IncomeVerificationOutput,
    CreditScoringInput,
    CreditScoringOutput,
    FraudDetectionInput,
    FraudDetectionOutput,
    ComplianceCheckInput,
    ComplianceCheckOutput,
    RiskAssessmentInput,
    RiskAssessmentOutput,
    FinalApprovalInput,
    FinalApprovalOutput,
    AgentRole,
    AgentStatus,
    AgentStateSnapshot
)

from schemas.decisions import (
    UnderwritingDecision,
    ApprovalDecision,
    RiskLevel,
    HumanReviewRequest,
    HumanReviewResponse,
    DecisionSummary,
    AuditableDecisionLog
)

from schemas.workflow import (
    WorkflowState,
    WorkflowStatus,
    WorkflowCheckpoint,
    WorkflowTransition,
    RetryPolicy,
    WorkflowMetrics
)

from schemas.tools import (
    ToolInvocation,
    ToolResponse,
    PayrollLookupRequest,
    PayrollLookupResponse,
    BankStatementRequest,
    BankStatementResponse,
    CreditBureauRequest,
    CreditBureauResponse,
    FraudServiceRequest,
    FraudServiceResponse,
    PolicyEngineRequest,
    PolicyEngineResponse,
    DocumentParserRequest,
    DocumentParserResponse,
    ToolRegistry,
    ToolName
)

__all__ = [
    # Application
    "LoanApplication",
    "LoanApplicationRequest",
    "EmploymentStatus",
    "DocumentType",
    "FraudSignals",
    # Evidence
    "EvidenceItem",
    "EvidenceLog",
    "EvidenceType",
    "VerificationStatus",
    # Agents
    "DocumentIntakeInput",
    "DocumentIntakeOutput",
    "IncomeVerificationInput",
    "IncomeVerificationOutput",
    "CreditScoringInput",
    "CreditScoringOutput",
    "FraudDetectionInput",
    "FraudDetectionOutput",
    "ComplianceCheckInput",
    "ComplianceCheckOutput",
    "RiskAssessmentInput",
    "RiskAssessmentOutput",
    "FinalApprovalInput",
    "FinalApprovalOutput",
    "AgentRole",
    "AgentStatus",
    "AgentStateSnapshot",
    # Decisions
    "UnderwritingDecision",
    "ApprovalDecision",
    "RiskLevel",
    "HumanReviewRequest",
    "HumanReviewResponse",
    "DecisionSummary",
    "AuditableDecisionLog",
    # Workflow
    "WorkflowState",
    "WorkflowStatus",
    "WorkflowCheckpoint",
    "WorkflowTransition",
    "RetryPolicy",
    "WorkflowMetrics",
    # Tools
    "ToolInvocation",
    "ToolResponse",
    "PayrollLookupRequest",
    "PayrollLookupResponse",
    "BankStatementRequest",
    "BankStatementResponse",
    "CreditBureauRequest",
    "CreditBureauResponse",
    "FraudServiceRequest",
    "FraudServiceResponse",
    "PolicyEngineRequest",
    "PolicyEngineResponse",
    "DocumentParserRequest",
    "DocumentParserResponse",
    "ToolRegistry",
    "ToolName"
]
