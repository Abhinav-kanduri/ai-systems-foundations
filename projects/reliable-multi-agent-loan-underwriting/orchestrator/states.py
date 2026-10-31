"""
Workflow states and state machine logic.
"""

from enum import Enum
from typing import Dict, List, Optional, Callable


class WorkflowStep(Enum):
    """Workflow steps."""
    SUBMITTED = "SUBMITTED"
    DOCUMENT_INTAKE = "DOCUMENT_INTAKE"
    PARALLEL_VERIFICATION = "PARALLEL_VERIFICATION"
    INCOME_VERIFICATION = "INCOME_VERIFICATION"
    CREDIT_SCORING = "CREDIT_SCORING"
    FRAUD_DETECTION = "FRAUD_DETECTION"
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    FINAL_DECISION = "FINAL_DECISION"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class StateTransitionMap:
    """Maps valid state transitions."""
    
    TRANSITIONS: Dict[WorkflowStep, List[WorkflowStep]] = {
        WorkflowStep.SUBMITTED: [WorkflowStep.DOCUMENT_INTAKE],
        WorkflowStep.DOCUMENT_INTAKE: [WorkflowStep.PARALLEL_VERIFICATION],
        WorkflowStep.PARALLEL_VERIFICATION: [
            WorkflowStep.INCOME_VERIFICATION,
            WorkflowStep.CREDIT_SCORING,
            WorkflowStep.FRAUD_DETECTION,
            WorkflowStep.COMPLIANCE_CHECK
        ],
        WorkflowStep.INCOME_VERIFICATION: [WorkflowStep.RISK_ASSESSMENT],
        WorkflowStep.CREDIT_SCORING: [WorkflowStep.RISK_ASSESSMENT],
        WorkflowStep.FRAUD_DETECTION: [WorkflowStep.RISK_ASSESSMENT],
        WorkflowStep.COMPLIANCE_CHECK: [WorkflowStep.RISK_ASSESSMENT],
        WorkflowStep.RISK_ASSESSMENT: [WorkflowStep.FINAL_DECISION],
        WorkflowStep.FINAL_DECISION: [
            WorkflowStep.HUMAN_REVIEW,
            WorkflowStep.COMPLETED,
            WorkflowStep.FAILED
        ],
        WorkflowStep.HUMAN_REVIEW: [
            WorkflowStep.COMPLETED,
            WorkflowStep.FAILED
        ],
        WorkflowStep.COMPLETED: [],
        WorkflowStep.FAILED: []
    }
    
    @classmethod
    def is_valid_transition(cls, from_step: WorkflowStep, to_step: WorkflowStep) -> bool:
        """Check if transition is valid."""
        return to_step in cls.TRANSITIONS.get(from_step, [])
    
    @classmethod
    def get_valid_transitions(cls, from_step: WorkflowStep) -> List[WorkflowStep]:
        """Get all valid next steps."""
        return cls.TRANSITIONS.get(from_step, [])


class ParallelAgents:
    """Agents that can run in parallel."""
    PARALLEL_STEPS = {
        WorkflowStep.PARALLEL_VERIFICATION: [
            WorkflowStep.INCOME_VERIFICATION,
            WorkflowStep.CREDIT_SCORING,
            WorkflowStep.FRAUD_DETECTION,
            WorkflowStep.COMPLIANCE_CHECK
        ]
    }
    
    @classmethod
    def get_parallel_agents(cls, step: WorkflowStep) -> List[WorkflowStep]:
        """Get agents that can run in parallel for this step."""
        return cls.PARALLEL_STEPS.get(step, [])
    
    @classmethod
    def is_parallel_step(cls, step: WorkflowStep) -> bool:
        """Check if this step involves parallel execution."""
        return step in cls.PARALLEL_STEPS
