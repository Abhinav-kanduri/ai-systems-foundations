"""
Workflow status and monitoring endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from orchestrator import WorkflowOrchestrator

logger = logging.getLogger(__name__)
router = APIRouter()

# Reference to workflows (would come from database in production)
workflows_store = {}


@router.get("/applications/{application_id}/status")
async def get_application_status(application_id: str) -> Dict[str, Any]:
    """
    Get current status of a loan application.
    
    Args:
        application_id: Application ID
        
    Returns:
        dict: Current workflow status
    """
    # In production, would query database
    matching_workflows = [
        w for w in workflows_store.values()
        if w.application_id == application_id
    ]
    
    if not matching_workflows:
        raise HTTPException(status_code=404, detail="Application status not found")
    
    workflow = matching_workflows[0]
    
    return {
        "application_id": application_id,
        "workflow_id": workflow.workflow_id,
        "current_step": workflow.state.current_step,
        "status": workflow.state.status,
        "completed_agents": workflow.state.completed_agents,
        "pending_agents": workflow.state.pending_agents,
        "retry_count": workflow.state.retry_count,
        "last_updated": workflow.state.updated_at,
        "trace_id": workflow.trace_id
    }


@router.get("/workflows/{workflow_id}/summary")
async def get_workflow_summary(workflow_id: str) -> Dict[str, Any]:
    """
    Get workflow execution summary.
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        dict: Workflow execution summary
    """
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    return workflow.get_workflow_summary()


@router.get("/workflows/{workflow_id}/trace")
async def get_workflow_trace(workflow_id: str) -> Dict[str, Any]:
    """
    Get detailed execution trace for a workflow.
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        dict: Detailed execution trace
    """
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    
    return {
        "trace_id": workflow.trace_id,
        "workflow_id": workflow.workflow_id,
        "application_id": workflow.application_id,
        "steps_completed": workflow.state.completed_agents,
        "evidence_count": len(workflow.evidence_log.evidence_items),
        "evidence_by_agent": {
            agent: len(workflow.evidence_log.get_evidence_by_agent(agent))
            for agent in set(e.agent_name for e in workflow.evidence_log.evidence_items)
        },
        "agent_results": workflow.agent_results,
        "created_at": workflow.state.created_at,
        "updated_at": workflow.state.updated_at
    }


@router.get("/workflows/{workflow_id}/evidence")
async def get_workflow_evidence(workflow_id: str) -> Dict[str, Any]:
    """
    Get all evidence from a workflow.
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        dict: All evidence items
    """
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    
    return {
        "workflow_id": workflow_id,
        "application_id": workflow.application_id,
        "evidence_items": [
            item.dict() for item in workflow.evidence_log.evidence_items
        ],
        "total_count": len(workflow.evidence_log.evidence_items)
    }
