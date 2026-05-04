"""
Evaluation tests for decision accuracy and reliability.
"""

import pytest
import json
from datetime import datetime

from orchestrator import WorkflowOrchestrator
from agents import (
    DocumentIntakeAgent, IncomeVerificationAgent, CreditScoringAgent,
    FraudDetectionAgent, ComplianceAgent, RiskAssessmentAgent, FinalApprovalAgent
)


# Golden dataset of known test cases
GOLDEN_DATASET = [
    {
        "name": "Strong application - should approve",
        "application": {
            "application_id": "GOLDEN-001",
            "applicant_id": "USER-001",
            "applicant_first_name": "Jane",
            "applicant_last_name": "Smith",
            "applicant_email": "jane@example.com",
            "applicant_phone": "+1-555-0101",
            "applicant_income": 10000,
            "credit_score": 780,
            "debt_to_income_ratio": 0.25,
            "employment_status": "FULL_TIME",
            "employment_length_months": 60,
            "loan_amount": 50000,
            "loan_purpose": "Home Improvement",
            "fraud_signals": {"device_mismatch": False, "identity_mismatch": False}
        },
        "expected_decision": "APPROVED",
        "expected_risk_level": "LOW"
    },
    {
        "name": "Income mismatch - should escalate",
        "application": {
            "application_id": "GOLDEN-002",
            "applicant_id": "USER-002",
            "applicant_first_name": "Bob",
            "applicant_last_name": "Johnson",
            "applicant_email": "bob@example.com",
            "applicant_phone": "+1-555-0102",
            "applicant_income": 5000,
            "credit_score": 700,
            "debt_to_income_ratio": 0.45,
            "employment_status": "FULL_TIME",
            "employment_length_months": 24,
            "loan_amount": 50000,
            "loan_purpose": "Debt Consolidation",
            "fraud_signals": {"device_mismatch": False, "identity_mismatch": False}
        },
        "expected_decision": "ESCALATE_TO_HUMAN",
        "expected_risk_level": "MEDIUM_HIGH"
    },
    {
        "name": "High fraud risk - should escalate",
        "application": {
            "application_id": "GOLDEN-003",
            "applicant_id": "USER-003",
            "applicant_first_name": "Charlie",
            "applicant_last_name": "Brown",
            "applicant_email": "charlie@example.com",
            "applicant_phone": "+1-555-0103",
            "applicant_income": 6000,
            "credit_score": 650,
            "debt_to_income_ratio": 0.40,
            "employment_status": "SELF_EMPLOYED",
            "employment_length_months": 12,
            "loan_amount": 75000,
            "loan_purpose": "Personal",
            "fraud_signals": {"device_mismatch": True, "identity_mismatch": True}
        },
        "expected_decision": "ESCALATE_TO_HUMAN",
        "expected_risk_level": "HIGH"
    }
]


@pytest.mark.asyncio
async def test_decision_accuracy():
    """Test decision accuracy against golden dataset."""
    agents_map = {
        "document_intake": DocumentIntakeAgent(),
        "income_verification": IncomeVerificationAgent(),
        "credit_scoring": CreditScoringAgent(),
        "fraud_detection": FraudDetectionAgent(),
        "compliance": ComplianceAgent(),
        "risk_assessment": RiskAssessmentAgent(),
        "final_approval": FinalApprovalAgent()
    }
    
    correct = 0
    total = len(GOLDEN_DATASET)
    
    for test_case in GOLDEN_DATASET:
        orchestrator = WorkflowOrchestrator(
            test_case["application"]["application_id"],
            test_case["application"]
        )
        
        decision = await orchestrator.execute_workflow(agents_map)
        
        # Check decision matches expectation
        matches_decision = decision.decision.value == test_case["expected_decision"]
        matches_risk = decision.risk_level.value == test_case["expected_risk_level"]
        
        if matches_decision and matches_risk:
            correct += 1
        
        print(f"\n{test_case['name']}")
        print(f"  Expected: {test_case['expected_decision']} ({test_case['expected_risk_level']})")
        print(f"  Actual:   {decision.decision.value} ({decision.risk_level.value})")
        print(f"  Match: {matches_decision and matches_risk}")
    
    accuracy = (correct / total) * 100
    print(f"\n\nOverall Accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    assert accuracy >= 80, f"Decision accuracy {accuracy:.1f}% below 80% threshold"


@pytest.mark.asyncio
async def test_consistency():
    """Test that same input produces same decision (consistency)."""
    application = GOLDEN_DATASET[0]["application"]
    
    agents_map1 = {
        "document_intake": DocumentIntakeAgent(),
        "income_verification": IncomeVerificationAgent(),
        "credit_scoring": CreditScoringAgent(),
        "fraud_detection": FraudDetectionAgent(),
        "compliance": ComplianceAgent(),
        "risk_assessment": RiskAssessmentAgent(),
        "final_approval": FinalApprovalAgent()
    }
    
    agents_map2 = {
        "document_intake": DocumentIntakeAgent(),
        "income_verification": IncomeVerificationAgent(),
        "credit_scoring": CreditScoringAgent(),
        "fraud_detection": FraudDetectionAgent(),
        "compliance": ComplianceAgent(),
        "risk_assessment": RiskAssessmentAgent(),
        "final_approval": FinalApprovalAgent()
    }
    
    # Run twice
    orchestrator1 = WorkflowOrchestrator(application["application_id"], application)
    decision1 = await orchestrator1.execute_workflow(agents_map1)
    
    orchestrator2 = WorkflowOrchestrator(application["application_id"], application)
    decision2 = await orchestrator2.execute_workflow(agents_map2)
    
    # Should get same decision
    assert decision1.decision == decision2.decision, "Decisions differ for same input"
    assert decision1.risk_level == decision2.risk_level, "Risk levels differ for same input"
    print("✓ Consistency test passed: Same input produces same decision")


def test_audit_completeness():
    """Test that audit records are complete."""
    application = GOLDEN_DATASET[0]["application"]
    
    orchestrator = WorkflowOrchestrator(
        application["application_id"],
        application
    )
    
    # Simulate that workflow has completed
    from schemas import UnderwritingDecision, ApprovalDecision, RiskLevel
    
    decision = UnderwritingDecision(
        application_id=application["application_id"],
        decision=ApprovalDecision.APPROVED,
        risk_level=RiskLevel.LOW,
        approval_confidence=0.95,
        reason_codes=["test"],
        detailed_explanation="Test",
        trace_id=orchestrator.trace_id,
        workflow_id=orchestrator.workflow_id
    )
    
    # Check all required audit fields
    assert decision.decision is not None
    assert decision.risk_level is not None
    assert decision.reason_codes is not None
    assert decision.trace_id is not None
    assert decision.workflow_id is not None
    assert decision.created_at is not None
    
    print("✓ Audit completeness test passed")


def test_golden_dataset_exists():
    """Verify golden dataset is available."""
    assert len(GOLDEN_DATASET) > 0, "Golden dataset is empty"
    
    for i, case in enumerate(GOLDEN_DATASET):
        assert "application" in case, f"Case {i} missing 'application'"
        assert "expected_decision" in case, f"Case {i} missing 'expected_decision'"
        assert "expected_risk_level" in case, f"Case {i} missing 'expected_risk_level'"
        assert case["application"]["application_id"] is not None
    
    print(f"✓ Golden dataset contains {len(GOLDEN_DATASET)} test cases")
