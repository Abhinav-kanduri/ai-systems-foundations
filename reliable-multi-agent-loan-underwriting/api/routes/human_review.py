"""
Human review workflow endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
import logging

from schemas import HumanReviewRequest, HumanReviewResponse, ApprovalDecision

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory review storage (would be database in production)
review_queue: Dict[str, HumanReviewRequest] = {}
review_responses: Dict[str, HumanReviewResponse] = {}


@router.get("/queue")
async def get_review_queue(limit: int = 10) -> Dict[str, Any]:
    """
    Get pending human review queue.
    
    Args:
        limit: Max items to return
        
    Returns:
        dict: Pending review items
    """
    pending = list(review_queue.values())[:limit]
    
    return {
        "total_pending": len(review_queue),
        "returned": len(pending),
        "items": [
            {
                "application_id": item.application_id,
                "workflow_id": item.workflow_id,
                "escalation_reason": item.escalation_reason,
                "priority": item.priority,
                "created_at": item.created_at
            }
            for item in pending
        ]
    }


@router.get("/applications/{application_id}/review-status")
async def get_review_status(application_id: str) -> Dict[str, Any]:
    """
    Get review status for an application.
    
    Args:
        application_id: Application ID
        
    Returns:
        dict: Review status and details
    """
    matching_reviews = [
        r for r in review_queue.values()
        if r.application_id == application_id
    ]
    
    if not matching_reviews:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review = matching_reviews[0]
    
    # Check if reviewed
    matching_responses = [
        r for r in review_responses.values()
        if r.application_id == application_id
    ]
    
    if matching_responses:
        response = matching_responses[0]
        status = "REVIEWED"
        review_data = {
            "reviewer_id": response.reviewer_id,
            "decision": response.decision,
            "reviewed_at": response.reviewed_at
        }
    else:
        status = "PENDING"
        review_data = {
            "requested_at": review.created_at,
            "escalation_reason": review.escalation_reason
        }
    
    return {
        "application_id": application_id,
        "status": status,
        "review": review_data
    }


@router.post("/applications/{application_id}/review")
async def submit_review(
    application_id: str,
    reviewer_id: str,
    decision: ApprovalDecision,
    override_reason: str,
    supporting_notes: str = None
) -> Dict[str, Any]:
    """
    Submit human review decision.
    
    Args:
        application_id: Application ID
        reviewer_id: ID of reviewer
        decision: Final decision (APPROVED, REJECTED, APPROVED_WITH_CONDITIONS)
        override_reason: Reason for override/review
        supporting_notes: Additional notes
        
    Returns:
        dict: Review submission confirmation
    """
    # Find matching review request
    matching_reviews = [
        r for r in review_queue.values()
        if r.application_id == application_id
    ]
    
    if not matching_reviews:
        raise HTTPException(status_code=404, detail="Review request not found")
    
    review_request = matching_reviews[0]
    
    # Create response
    response = HumanReviewResponse(
        application_id=application_id,
        decision_id=review_request.decision_id,
        reviewer_id=reviewer_id,
        decision=decision,
        override_reason=override_reason,
        supporting_notes=supporting_notes
    )
    
    review_responses[response.review_id] = response
    
    # Remove from queue
    del review_queue[review_request.application_id]
    
    logger.info(f"Review submitted for {application_id}: {decision}")
    
    return {
        "review_id": response.review_id,
        "application_id": application_id,
        "decision": decision,
        "reviewed_at": response.reviewed_at
    }


@router.get("/reviews/{review_id}")
async def get_review(review_id: str) -> Dict[str, Any]:
    """
    Get a specific review response.
    
    Args:
        review_id: Review response ID
        
    Returns:
        dict: Review details
    """
    matching = [r for r in review_responses.values() if r.review_id == review_id]
    
    if not matching:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review = matching[0]
    
    return {
        "review_id": review.review_id,
        "application_id": review.application_id,
        "reviewer_id": review.reviewer_id,
        "decision": review.decision,
        "override_reason": review.override_reason,
        "reviewed_at": review.reviewed_at
    }
