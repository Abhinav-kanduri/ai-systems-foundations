"""
Final Approval Agent - makes final underwriting decision.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType


class FinalApprovalAgent(BaseAgent):
    """Agent for final approval recommendation."""
    
    def __init__(self):
        super().__init__(
            agent_name="FinalApprovalAgent",
            agent_version="1.0.0"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute final approval decision.
        
        Args:
            application_id: Application ID
            applicant_income: Income
            loan_amount: Loan amount
            risk_assessment_result: Risk assessment from upstream agent
            
        Returns:
            dict: Final decision (APPROVED, REJECTED, or ESCALATE_TO_HUMAN)
        """
        application_id = kwargs.get("application_id")
        loan_amount = kwargs.get("loan_amount", 0)
        
        self.validate_input(kwargs, ["application_id"])
        
        risk_result = kwargs.get("risk_assessment_result", {})
        risk_level = risk_result.get("overall_risk_level", "MEDIUM")
        risk_score = risk_result.get("risk_score", 0.5)
        
        # Decision logic based on risk level
        decision = None
        reason_codes = []
        escalation_reason = None
        confidence = 0.0
        
        if risk_level == "LOW":
            decision = "APPROVED"
            reason_codes = ["low_risk", "standard_approval"]
            confidence = 0.95
        elif risk_level == "MEDIUM":
            decision = "APPROVED"
            reason_codes = ["medium_risk", "approved_with_monitoring"]
            confidence = 0.80
        elif risk_level == "MEDIUM_HIGH":
            decision = "ESCALATE_TO_HUMAN"
            reason_codes = ["medium_high_risk", "requires_manual_review"]
            escalation_reason = "Risk level requires human judgment"
            confidence = 0.70
        else:  # HIGH
            decision = "REJECTED"
            reason_codes = ["high_risk", "exceeds_risk_threshold"]
            confidence = 0.85
        
        # Add specific reason codes based on factors
        if "income_risk" in risk_result.get("risk_factors", {}):
            income_risk = risk_result["risk_factors"]["income_risk"]
            if income_risk > 0.3:
                reason_codes.append("income_verification_concerns")
        
        if "dti_risk" in risk_result.get("risk_factors", {}):
            dti_risk = risk_result["risk_factors"]["dti_risk"]
            if dti_risk > 0.3:
                reason_codes.append("high_debt_to_income_ratio")
        
        result = {
            "application_id": application_id,
            "decision": decision,
            "risk_level": risk_level,
            "reason_codes": list(set(reason_codes)),  # Remove duplicates
            "approval_confidence": confidence,
            "human_review_required": decision == "ESCALATE_TO_HUMAN",
            "escalation_reason": escalation_reason
        }
        
        return result
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.APPROVAL_DECISION,
            description=f"Final decision: {agent_output['decision']} ({agent_output['risk_level']} risk)",
            key_findings={
                "decision": agent_output["decision"],
                "risk_level": agent_output["risk_level"],
                "reason_codes": agent_output["reason_codes"]
            },
            supporting_data={
                "escalation_reason": agent_output.get("escalation_reason")
            },
            confidence=agent_output["approval_confidence"],
            source_refs=["risk_assessment", "policy_engine"],
            reasoning=f"Decision: {agent_output['decision']}. Reasons: {', '.join(agent_output['reason_codes'])}"
        )


__all__ = ["FinalApprovalAgent"]
