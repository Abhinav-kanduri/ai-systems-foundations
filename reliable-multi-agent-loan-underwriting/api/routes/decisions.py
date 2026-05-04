"""
Decision retrieval endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory decision storage (would be database in production)
decisions_store: Dict[str, Dict[str, Any]] = {}


@router.get("/applications/{application_id}/decision")
async def get_application_decision(application_id: str) -> Dict[str, Any]:
    """
    Get final underwriting decision for an application.
    
    Args:
        application_id: Application ID
        
    Returns:
        dict: Final decision and supporting evidence
    """
    if application_id not in decisions_store:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    decision = decisions_store[application_id]
    
    return {
        "application_id": application_id,
        "decision": decision.get("decision"),
        "risk_level": decision.get("risk_level"),
        "reason_codes": decision.get("reason_codes", []),
        "detailed_explanation": decision.get("detailed_explanation"),
        "approval_confidence": decision.get("approval_confidence"),
        "trace_id": decision.get("trace_id"),
        "human_review_required": decision.get("human_review_required", False),
        "audit_status": decision.get("audit_status", "COMPLETE"),
        "created_at": decision.get("created_at")
    }


@router.get("/applications/{application_id}/decision/evidence")
async def get_decision_evidence(application_id: str) -> Dict[str, Any]:
    """
    Get all supporting evidence for a decision.
    
    Args:
        application_id: Application ID
        
    Returns:
        dict: All evidence backing the decision
    """
    if application_id not in decisions_store:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    decision = decisions_store[application_id]
    
    return {
        "application_id": application_id,
        "decision": decision.get("decision"),
        "agent_evidence": decision.get("agent_evidence", {}),
        "trace_id": decision.get("trace_id")
    }


@router.get("/decisions/{decision_id}")
async def get_decision_by_id(decision_id: str) -> Dict[str, Any]:
    """
    Get a specific decision record.
    
    Args:
        decision_id: Decision ID
        
    Returns:
        dict: Decision record
    """
    # In production, would query database by decision_id
    raise HTTPException(status_code=404, detail="Decision not found")
