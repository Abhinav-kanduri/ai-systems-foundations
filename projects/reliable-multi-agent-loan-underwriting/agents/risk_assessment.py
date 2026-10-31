"""
Risk Assessment Agent - aggregates evidence and assigns risk level.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType


class RiskAssessmentAgent(BaseAgent):
    """Agent for aggregating evidence and assigning overall risk level."""
    
    def __init__(self):
        super().__init__(
            agent_name="RiskAssessmentAgent",
            agent_version="1.0.0"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute risk assessment.
        
        Args:
            application_id: Application ID
            applicant_income: Annual income
            loan_amount: Loan amount
            debt_to_income_ratio: DTI ratio
            income_verification_result: Income verification evidence
            credit_scoring_result: Credit scoring evidence
            fraud_detection_result: Fraud detection evidence
            compliance_result: Compliance check evidence
            
        Returns:
            dict: Risk assessment with overall risk level
        """
        application_id = kwargs.get("application_id")
        applicant_income = kwargs.get("applicant_income", 0)
        loan_amount = kwargs.get("loan_amount", 0)
        dti_ratio = kwargs.get("debt_to_income_ratio", 0)
        
        self.validate_input(kwargs, ["application_id"])
        
        # Extract results from upstream agents
        income_result = kwargs.get("income_verification_result", {})
        credit_result = kwargs.get("credit_scoring_result", {})
        fraud_result = kwargs.get("fraud_detection_result", {})
        compliance_result = kwargs.get("compliance_result", {})
        
        # Compute risk factors (0.0 = lowest risk, 1.0 = highest risk)
        risk_factors = {}
        
        # Income risk
        if income_result.get("verification_status") == "MISMATCH":
            risk_factors["income_risk"] = 0.4
        elif income_result.get("verification_status") == "INSUFFICIENT_EVIDENCE":
            risk_factors["income_risk"] = 0.3
        else:
            risk_factors["income_risk"] = 0.1
        
        # Credit risk
        credit_risk_level = credit_result.get("credit_risk_level", "MEDIUM")
        risk_factors["credit_risk"] = {
            "LOW": 0.1,
            "MEDIUM": 0.3,
            "MEDIUM_HIGH": 0.6,
            "HIGH": 0.8
        }.get(credit_risk_level, 0.5)
        
        # DTI risk
        if dti_ratio > 0.43:
            risk_factors["dti_risk"] = 0.5
        elif dti_ratio > 0.36:
            risk_factors["dti_risk"] = 0.3
        else:
            risk_factors["dti_risk"] = 0.1
        
        # Fraud risk
        fraud_risk_score = fraud_result.get("fraud_risk_score", 0.0)
        risk_factors["fraud_risk"] = fraud_risk_score
        
        # Compliance risk
        if not compliance_result.get("regulatory_compliance", True):
            risk_factors["compliance_risk"] = 0.7
        else:
            risk_factors["compliance_risk"] = 0.0
        
        # Calculate weighted overall risk (equally weighted for simplicity)
        overall_risk_score = sum(risk_factors.values()) / len(risk_factors) if risk_factors else 0.5
        
        # Determine risk level
        if overall_risk_score < 0.2:
            risk_level = "LOW"
        elif overall_risk_score < 0.4:
            risk_level = "MEDIUM"
        elif overall_risk_score < 0.6:
            risk_level = "MEDIUM_HIGH"
        else:
            risk_level = "HIGH"
        
        # Generate summary
        risk_summary = f"Overall risk level: {risk_level} (score: {overall_risk_score:.2f}). "
        risk_summary += f"Key factors: "
        risk_summary += f"Income ({risk_factors.get('income_risk', 0):.2f}), "
        risk_summary += f"Credit ({risk_factors.get('credit_risk', 0):.2f}), "
        risk_summary += f"DTI ({risk_factors.get('dti_risk', 0):.2f})"
        
        result = {
            "application_id": application_id,
            "overall_risk_level": risk_level,
            "risk_score": overall_risk_score,
            "risk_factors": risk_factors,
            "risk_summary": risk_summary,
            "confidence": 0.85,
            "requires_escalation": risk_level in ["MEDIUM_HIGH", "HIGH"]
        }
        
        return result
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.RISK_CALCULATION,
            description=f"Risk assessment: {agent_output['overall_risk_level']} risk (score: {agent_output['risk_score']:.2f})",
            key_findings={
                "overall_risk_level": agent_output["overall_risk_level"],
                "risk_score": agent_output["risk_score"]
            },
            supporting_data={
                "risk_factors": agent_output["risk_factors"],
                "risk_summary": agent_output["risk_summary"]
            },
            confidence=agent_output["confidence"],
            source_refs=["income_verification", "credit_scoring", "fraud_detection", "compliance"],
            reasoning=agent_output["risk_summary"]
        )
