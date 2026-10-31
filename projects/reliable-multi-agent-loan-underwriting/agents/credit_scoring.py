"""
Credit Scoring Agent - evaluates credit risk and history.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType


class CreditScoringAgent(BaseAgent):
    """Agent for credit scoring and risk assessment."""
    
    def __init__(self):
        super().__init__(
            agent_name="CreditScoringAgent",
            agent_version="1.0.0"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute credit scoring.
        
        Args:
            application_id: Application ID
            applicant_id: Applicant ID
            credit_score: Credit score (if available)
            loan_amount: Requested loan amount
            
        Returns:
            dict: Credit assessment with risk level
        """
        application_id = kwargs.get("application_id")
        credit_score = kwargs.get("credit_score", 650)
        loan_amount = kwargs.get("loan_amount", 10000)
        
        self.validate_input(kwargs, ["application_id", "applicant_id"])
        
        # Determine risk level based on credit score
        if credit_score >= 750:
            risk_level = "LOW"
            confidence = 0.95
        elif credit_score >= 700:
            risk_level = "MEDIUM"
            confidence = 0.90
        elif credit_score >= 650:
            risk_level = "MEDIUM_HIGH"
            confidence = 0.85
        else:
            risk_level = "HIGH"
            confidence = 0.80
        
        # Risk factors
        risk_factors = []
        if credit_score < 700:
            risk_factors.append("Below prime credit score")
        if credit_score < 650:
            risk_factors.append("Subprime credit score")
        
        # Simulate credit history retrieval
        credit_history_months = min(120, max(6, int(650 + (credit_score - 700) * 2)))
        
        result = {
            "application_id": application_id,
            "credit_score": credit_score,
            "credit_risk_level": risk_level,
            "risk_factors": risk_factors,
            "credit_history_length_months": credit_history_months,
            "confidence": confidence,
            "reason_codes": [
                f"credit_score_{credit_score}",
                f"risk_level_{risk_level}",
                f"credit_history_{credit_history_months}_months"
            ]
        }
        
        return result
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.CREDIT_CHECK,
            description=f"Credit scoring: {agent_output['credit_risk_level']} risk (score: {agent_output['credit_score']})",
            key_findings={
                "credit_score": agent_output["credit_score"],
                "risk_level": agent_output["credit_risk_level"],
                "credit_history_months": agent_output["credit_history_length_months"]
            },
            supporting_data={
                "risk_factors": agent_output["risk_factors"]
            },
            confidence=agent_output["confidence"],
            source_refs=["credit_bureau"],
            reasoning=f"Credit score of {agent_output['credit_score']} indicates {agent_output['credit_risk_level']} risk"
        )
