"""
Income Verification Agent - verifies income through multiple sources.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base import BaseAgent
from schemas.evidence import EvidenceItem, EvidenceType, VerificationStatus


class IncomeVerificationAgent(BaseAgent):
    """Agent for income verification through multiple data sources."""
    
    def __init__(self):
        super().__init__(
            agent_name="IncomeVerificationAgent",
            agent_version="1.0.0"
        )
        self.confidence_threshold = 0.75
        self.max_variance = 0.15  # 15% variance tolerance
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute income verification.
        
        Args:
            application_id: Application ID
            applicant_id: Applicant ID
            stated_income: Stated monthly income
            paystub_data: Paystub data dict
            bank_statement_data: Bank statement data dict
            
        Returns:
            dict: Verification result with confidence
        """
        application_id = kwargs.get("application_id")
        stated_income = kwargs.get("stated_income", 0)
        paystub_data = kwargs.get("paystub_data", {})
        bank_data = kwargs.get("bank_statement_data", {})
        
        self.validate_input(kwargs, ["application_id", "applicant_id", "stated_income"])
        
        # Get verified income from sources
        paystub_income = paystub_data.get("gross_monthly_salary", 0)
        bank_income = bank_data.get("average_monthly_deposit", 0)
        
        # Calculate average verified income
        verified_sources = []
        if paystub_income > 0:
            verified_sources.append(paystub_income)
        if bank_income > 0:
            verified_sources.append(bank_income)
        
        if not verified_sources:
            verified_income = 0
            confidence = 0.0
            verification_status = VerificationStatus.INSUFFICIENT_EVIDENCE
        else:
            verified_income = sum(verified_sources) / len(verified_sources)
            variance = abs(verified_income - stated_income) / stated_income if stated_income > 0 else 0
            
            if variance < self.max_variance:
                verification_status = VerificationStatus.MATCH
                confidence = 1.0 - (variance / self.max_variance)
            else:
                verification_status = VerificationStatus.MISMATCH
                confidence = max(0.3, 1.0 - variance)
        
        variance_pct = ((verified_income - stated_income) / stated_income * 100) if stated_income > 0 else 0
        
        discrepancies = []
        if abs(variance_pct) > 10:
            discrepancies.append(f"Income variance: {variance_pct:.1f}%")
        
        if paystub_income > 0 and bank_income > 0:
            paystub_vs_bank = abs(paystub_income - bank_income) / paystub_income
            if paystub_vs_bank > 0.15:
                discrepancies.append(f"Paystub vs bank statement mismatch: {paystub_vs_bank:.1%}")
        
        result = {
            "application_id": application_id,
            "verification_status": verification_status.value,
            "stated_income": stated_income,
            "verified_income": verified_income,
            "variance_percentage": variance_pct,
            "verification_source": ["paystub", "bank_statement"] if verified_sources else [],
            "confidence": confidence,
            "reason_codes": [
                "income_match" if verification_status == VerificationStatus.MATCH else "income_mismatch",
                f"verified_from_{len(verified_sources)}_sources"
            ],
            "requires_escalation": verification_status == VerificationStatus.MISMATCH or confidence < self.confidence_threshold,
            "discrepancies": discrepancies
        }
        
        return result
    
    def generate_evidence(self, agent_output: Dict[str, Any]) -> EvidenceItem:
        """Generate evidence record from agent output."""
        return EvidenceItem(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            evidence_type=EvidenceType.INCOME_VERIFICATION,
            description=f"Income verification: {agent_output['verification_status']}",
            key_findings={
                "stated_income": agent_output["stated_income"],
                "verified_income": agent_output["verified_income"],
                "variance": agent_output["variance_percentage"]
            },
            supporting_data={
                "sources": agent_output["verification_source"],
                "discrepancies": agent_output.get("discrepancies", [])
            },
            confidence=agent_output["confidence"],
            source_refs=agent_output["verification_source"],
            reasoning=f"Verified income from {len(agent_output['verification_source'])} sources with {agent_output['confidence']:.0%} confidence"
        )
