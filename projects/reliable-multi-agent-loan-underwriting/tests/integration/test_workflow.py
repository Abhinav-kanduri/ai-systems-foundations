"""
Integration tests for workflow orchestration.
"""

import pytest
from datetime import datetime

from orchestrator import WorkflowOrchestrator, WorkflowStep
from agents import (
    DocumentIntakeAgent, IncomeVerificationAgent, CreditScoringAgent,
    FraudDetectionAgent, ComplianceAgent, RiskAssessmentAgent, FinalApprovalAgent
)
from schemas import LoanApplicationRequest, EmploymentStatus, FraudSignals


@pytest.fixture
def sample_application():
    """Create sample loan application for testing."""
    return {
        "application_id": "APP-1001",
        "applicant_id": "USER-1001",
        "applicant_first_name": "John",
        "applicant_last_name": "Doe",
        "applicant_email": "john@example.com",
        "applicant_phone": "+1-555-0100",
        "applicant_income": 8500,
        "credit_score": 720,
        "debt_to_income_ratio": 0.43,
        "employment_status": "FULL_TIME",
        "employment_length_months": 36,
        "loan_amount": 50000,
        "loan_purpose": "Home Improvement",
        "fraud_signals": {
            "device_mismatch": False,
            "identity_mismatch": False
        }
    }


@pytest.mark.asyncio
async def test_workflow_initialization(sample_application):
    """Test workflow initialization."""
    orchestrator = WorkflowOrchestrator(
        sample_application["application_id"],
        sample_application
    )
    
    assert orchestrator.workflow_id is not None
    assert orchestrator.application_id == sample_application["application_id"]
    assert orchestrator.state.current_step == "SUBMITTED"
    assert len(orchestrator.agent_results) == 0


@pytest.mark.asyncio
async def test_workflow_execution_happy_path(sample_application):
    """Test complete workflow execution."""
    orchestrator = WorkflowOrchestrator(
        sample_application["application_id"],
        sample_application
    )
    
    agents_map = {
        "document_intake": DocumentIntakeAgent(),
        "income_verification": IncomeVerificationAgent(),
        "credit_scoring": CreditScoringAgent(),
        "fraud_detection": FraudDetectionAgent(),
        "compliance": ComplianceAgent(),
        "risk_assessment": RiskAssessmentAgent(),
        "final_approval": FinalApprovalAgent()
    }
    
    decision = await orchestrator.execute_workflow(agents_map)
    
    assert decision is not None
    assert decision.application_id == sample_application["application_id"]
    assert decision.decision in ["APPROVED", "REJECTED", "ESCALATE_TO_HUMAN"]
    assert decision.trace_id is not None
    assert len(decision.reason_codes) > 0


@pytest.mark.asyncio
async def test_workflow_checkpoint_creation(sample_application):
    """Test checkpoint creation during workflow."""
    orchestrator = WorkflowOrchestrator(
        sample_application["application_id"],
        sample_application
    )
    
    # Manually execute a step to trigger checkpoint
    agents_map = {
        "document_intake": DocumentIntakeAgent(),
    }
    
    agent = agents_map["document_intake"]
    agent_input = orchestrator._prepare_agent_input(WorkflowStep.DOCUMENT_INTAKE)
    result = await agent.run(**agent_input)
    
    orchestrator.agent_results["DOCUMENT_INTAKE"] = result
    orchestrator._create_checkpoint()
    
    assert len(orchestrator.checkpoint_history) > 0
    checkpoint = orchestrator.checkpoint_history[-1]
    assert checkpoint.workflow_id == orchestrator.workflow_id
    assert checkpoint.current_step == WorkflowStep.DOCUMENT_INTAKE


def test_workflow_summary(sample_application):
    """Test workflow summary generation."""
    orchestrator = WorkflowOrchestrator(
        sample_application["application_id"],
        sample_application
    )
    
    summary = orchestrator.get_workflow_summary()
    
    assert summary["workflow_id"] == orchestrator.workflow_id
    assert summary["application_id"] == sample_application["application_id"]
    assert "current_step" in summary
    assert "status" in summary
    assert "completed_agents" in summary
