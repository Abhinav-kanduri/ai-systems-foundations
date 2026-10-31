"""
Fraud Detection Agent - detects fraud signals and risks.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType


class FraudDetectionAgent(BaseAgent):
    """Agent for fraud detection and risk assessment."""
    
    def __init__(self):
        super().__init__(
            agent_name="FraudDetectionAgent",
            agent_version="1.0.0"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute fraud detection.
        
        Args:
            application_id: Application ID
            applicant_id: Applicant ID
            applicant_email: Email address
            applicant_phone: Phone number
            fraud_signals: Dict of fraud signal indicators
            
        Returns:
            dict: Fraud assessment with risk score
        """
        application_id = kwargs.get("application_id")
        fraud_signals = kwargs.get("fraud_signals", {})
        
        self.validate_input(kwargs, ["application_id", "applicant_id"])
        
        # Analyze fraud signals
        fraud_flags = []
        fraud_risk_score = 0.0
        
        if fraud_signals.get("device_mismatch"):
            fraud_flags.append("Device location anomaly")
            fraud_risk_score += 0.25
        
        if fraud_signals.get("identity_mismatch"):
            fraud_flags.append("Identity verification mismatch")
            fraud_risk_score += 0.30
        
        if fraud_signals.get("velocity_check"):
            fraud_flags.append("Unusual submission velocity")
            fraud_risk_score += 0.15
        
        if fraud_signals.get("duplicate_application"):
            fraud_flags.append("Potential duplicate application")
            fraud_risk_score += 0.35
        
        # Determine risk level
        if fraud_risk_score >= 0.50:
            risk_level = "HIGH"
            fraud_detected = True
        elif fraud_risk_score >= 0.25:
            risk_level = "MEDIUM"
            fraud_detected = False
        else:
            risk_level = "LOW"
            fraud_detected = False
        
        # Confidence is higher with more signals
        confidence = min(0.95, 0.7 + (len(fraud_flags) * 0.1))
        
        result = {
            "application_id": application_id,
            "fraud_risk_score": fraud_risk_score,
            "fraud_detected": fraud_detected,
            "fraud_flags": fraud_flags,
            "blacklist_match": False,  # Simulated
            "risk_level": risk_level,
            "confidence": confidence,
            "reason_codes": [
                f"fraud_risk_{risk_level}",
                f"fraud_flags_{len(fraud_flags)}"
            ] + fraud_flags,
            "requires_escalation": fraud_detected or fraud_risk_score >= 0.25
        }
        
        return result
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        flags_summary = ", ".join(agent_output["fraud_flags"]) if agent_output["fraud_flags"] else "None"
        
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.FRAUD_ASSESSMENT,
            description=f"Fraud detection: {agent_output['risk_level']} risk (score: {agent_output['fraud_risk_score']:.2f})",
            key_findings={
                "fraud_risk_score": agent_output["fraud_risk_score"],
                "risk_level": agent_output["risk_level"],
                "fraud_detected": agent_output["fraud_detected"]
            },
            supporting_data={
                "fraud_flags": agent_output["fraud_flags"]
            },
            confidence=agent_output["confidence"],
            source_refs=["fraud_detection_service"],
            reasoning=f"Identified {len(agent_output['fraud_flags'])} fraud indicators: {flags_summary}"
        )
