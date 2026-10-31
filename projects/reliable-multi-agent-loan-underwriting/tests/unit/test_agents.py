"""
Unit tests for agents.
"""

import pytest
from datetime import datetime

from agents import DocumentIntakeAgent, IncomeVerificationAgent, CreditScoringAgent
from schemas.evidence import EvidenceType


@pytest.mark.asyncio
async def test_document_intake_agent():
    """Test document intake agent."""
    agent = DocumentIntakeAgent()
    
    result = await agent.execute(
        application_id="APP-001",
        applicant_id="USER-001",
        documents_content={
            "paystub": "Monthly salary information...",
            "bank_statement": "Bank transaction history...",
            "id_proof": "Driver's license..."
        }
    )
    
    assert result["application_id"] == "APP-001"
    assert "extracted_fields" in result
    assert result["confidence"] > 0
    assert isinstance(result["confidence"], float)


@pytest.mark.asyncio
async def test_income_verification_agent():
    """Test income verification agent."""
    agent = IncomeVerificationAgent()
    
    result = await agent.execute(
        application_id="APP-001",
        applicant_id="USER-001",
        stated_income=5000,
        employment_status="FULL_TIME",
        employment_length_months=36,
        paystub_data={"gross_monthly_salary": 5000},
        bank_statement_data={"average_monthly_deposit": 5100}
    )
    
    assert result["application_id"] == "APP-001"
    assert result["verification_status"] in ["MATCH", "MISMATCH", "INSUFFICIENT_EVIDENCE"]
    assert "variance_percentage" in result
    assert result["confidence"] > 0


@pytest.mark.asyncio
async def test_credit_scoring_agent():
    """Test credit scoring agent."""
    agent = CreditScoringAgent()
    
    result = await agent.execute(
        application_id="APP-001",
        applicant_id="USER-001",
        credit_score=750,
        loan_amount=50000,
        loan_purpose="Home Improvement"
    )
    
    assert result["application_id"] == "APP-001"
    assert result["credit_score"] == 750
    assert result["credit_risk_level"] in ["LOW", "MEDIUM", "MEDIUM_HIGH", "HIGH"]
    assert result["confidence"] > 0


def test_evidence_generation():
    """Test evidence generation from agent output."""
    agent = DocumentIntakeAgent()
    
    output = {
        "application_id": "APP-001",
        "extracted_fields": {"name": "John Doe"},
        "document_quality": {"paystub": 0.95},
        "missing_documents": [],
        "processing_errors": [],
        "confidence": 0.95,
        "requires_manual_review": False
    }
    
    evidence = agent.generate_evidence(output)
    
    assert evidence.agent_name == "DocumentIntakeAgent"
    assert evidence.evidence_type == EvidenceType.DOCUMENT_EXTRACTION
    assert evidence.confidence == 0.95
    assert len(evidence.source_refs) > 0
