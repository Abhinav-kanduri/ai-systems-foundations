"""
Application submission and management endpoints.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging

from schemas import LoanApplicationRequest, LoanApplication
from orchestrator import WorkflowOrchestrator
from agents import (
    DocumentIntakeAgent, IncomeVerificationAgent, CreditScoringAgent,
    FraudDetectionAgent, ComplianceAgent, RiskAssessmentAgent, FinalApprovalAgent
)

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage (would be replaced with database in production)
applications_store: Dict[str, LoanApplication] = {}
workflows_store: Dict[str, WorkflowOrchestrator] = {}


@router.post("/")
async def submit_application(
    request: LoanApplicationRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Submit a new loan application.
    
    Args:
        request: Loan application submission
        background_tasks: FastAPI background task handler
        
    Returns:
        dict: Application ID, workflow ID, and status
    """
    try:
        # Create application record
        application = LoanApplication(**request.dict())
        applications_store[application.application_id] = application
        
        # Initialize orchestrator
        orchestrator = WorkflowOrchestrator(
            application.application_id,
            application.dict()
        )
        workflows_store[orchestrator.workflow_id] = orchestrator
        
        # Start workflow execution in background
        background_tasks.add_task(
            execute_workflow,
            orchestrator,
            application
        )
        
        logger.info(f"Application {application.application_id} submitted, workflow {orchestrator.workflow_id} started")
        
        return {
            "application_id": application.application_id,
            "workflow_id": orchestrator.workflow_id,
            "status": "STARTED",
            "trace_id": orchestrator.trace_id
        }
    
    except Exception as e:
        logger.error(f"Failed to submit application: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{application_id}")
async def get_application(application_id: str) -> Dict[str, Any]:
    """
    Get application details.
    
    Args:
        application_id: Application ID
        
    Returns:
        dict: Application details
    """
    if application_id not in applications_store:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application = applications_store[application_id]
    return application.dict()


@router.get("")
async def list_applications(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    List all applications.
    
    Args:
        limit: Number of results to return
        offset: Offset for pagination
        
    Returns:
        dict: List of applications
    """
    apps = list(applications_store.values())
    total = len(apps)
    results = apps[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "applications": [app.dict() for app in results]
    }


async def execute_workflow(
    orchestrator: WorkflowOrchestrator,
    application: LoanApplication
) -> None:
    """
    Execute the complete underwriting workflow.
    
    Args:
        orchestrator: Workflow orchestrator instance
        application: Loan application
    """
    try:
        # Initialize agents
        agents_map = {
            "document_intake": DocumentIntakeAgent(),
            "income_verification": IncomeVerificationAgent(),
            "credit_scoring": CreditScoringAgent(),
            "fraud_detection": FraudDetectionAgent(),
            "compliance": ComplianceAgent(),
            "risk_assessment": RiskAssessmentAgent(),
            "final_approval": FinalApprovalAgent()
        }
        
        # Execute workflow
        decision = await orchestrator.execute_workflow(agents_map)
        
        # Store decision (in real system, would save to database)
        logger.info(f"Workflow {orchestrator.workflow_id} completed with decision: {decision.decision}")
        
    except Exception as e:
        logger.error(f"Workflow execution failed for {orchestrator.workflow_id}: {str(e)}")
        raise
