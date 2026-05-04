"""
Agents package initialization.
"""

from agents.base import BaseAgent
from agents.document_intake import DocumentIntakeAgent
from agents.income_verification import IncomeVerificationAgent
from agents.credit_scoring import CreditScoringAgent
from agents.fraud_detection import FraudDetectionAgent
from agents.compliance import ComplianceAgent
from agents.risk_assessment import RiskAssessmentAgent
from agents.final_approval import FinalApprovalAgent

__all__ = [
    "BaseAgent",
    "DocumentIntakeAgent",
    "IncomeVerificationAgent",
    "CreditScoringAgent",
    "FraudDetectionAgent",
    "ComplianceAgent",
    "RiskAssessmentAgent",
    "FinalApprovalAgent"
]
