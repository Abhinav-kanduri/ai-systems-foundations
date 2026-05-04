"""
Compliance Agent - checks regulatory and policy compliance.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType


class ComplianceAgent(BaseAgent):
    """Agent for compliance checking and regulatory validation."""
    
    def __init__(self):
        super().__init__(
            agent_name="ComplianceAgent",
            agent_version="1.0.0"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute compliance checks.
        
        Args:
            application_id: Application ID
            applicant_first_name: First name
            applicant_last_name: Last name
            applicant_email: Email
            loan_amount: Loan amount
            
        Returns:
            dict: Compliance assessment
        """
        application_id = kwargs.get("application_id")
        loan_amount = kwargs.get("loan_amount", 0)
        
        self.validate_input(kwargs, [
            "application_id",
            "applicant_first_name",
            "applicant_last_name"
        ])
        
        # Simulated compliance checks
        policy_violations = []
        warnings = []
        
        # AML check (simulated)
        aml_check_passed = True
        
        # Sanction check (simulated)
        sanction_check_passed = True
        
        # Loan amount compliance
        if loan_amount > 100000:
            warnings.append("Large loan amount - additional verification may be required")
        
        # Overall compliance
        regulatory_compliance = aml_check_passed and sanction_check_passed
        
        confidence = 0.95 if regulatory_compliance else 0.85
        
        result = {
            "application_id": application_id,
            "sanction_check_passed": sanction_check_passed,
            "aml_check_passed": aml_check_passed,
            "regulatory_compliance": regulatory_compliance,
            "policy_violations": policy_violations,
            "regulatory_notes": "All regulatory checks passed" if regulatory_compliance else "Compliance review needed",
            "confidence": confidence,
            "requires_manual_review": len(policy_violations) > 0
        }
        
        return result
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.COMPLIANCE_CHECK,
            description=f"Compliance check: {'Passed' if agent_output['regulatory_compliance'] else 'Review needed'}",
            key_findings={
                "aml_check_passed": agent_output["aml_check_passed"],
                "sanction_check_passed": agent_output["sanction_check_passed"],
                "regulatory_compliance": agent_output["regulatory_compliance"]
            },
            supporting_data={
                "policy_violations": agent_output["policy_violations"],
                "regulatory_notes": agent_output.get("regulatory_notes")
            },
            confidence=agent_output["confidence"],
            source_refs=["compliance_engine", "regulatory_database"],
            reasoning=f"All compliance checks: {'passed' if agent_output['regulatory_compliance'] else 'failed or require review'}"
        )
