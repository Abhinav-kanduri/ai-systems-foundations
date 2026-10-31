"""
Workflow orchestration engine.
"""

import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

from schemas import (
    WorkflowState, WorkflowStatus, WorkflowCheckpoint, 
    EvidenceLog, UnderwritingDecision, ApprovalDecision, RiskLevel
)
from orchestrator.states import WorkflowStep, StateTransitionMap, ParallelAgents


class WorkflowOrchestrator:
    """Manages multi-agent workflow orchestration."""
    
    def __init__(self, application_id: str, applicant_data: Dict[str, Any]):
        """Initialize orchestrator."""
        self.workflow_id = f"wf-{uuid.uuid4().hex[:12]}"
        self.application_id = application_id
        self.applicant_data = applicant_data
        
        self.state = WorkflowState(
            workflow_id=self.workflow_id,
            application_id=application_id,
            current_step=WorkflowStatus.SUBMITTED,
            status="RUNNING"
        )
        
        self.evidence_log = EvidenceLog(
            application_id=application_id,
            workflow_id=self.workflow_id
        )
        
        self.checkpoint_history: List[WorkflowCheckpoint] = []
        self.agent_results: Dict[str, Any] = {}
        
        self.trace_id = f"trace-{uuid.uuid4().hex[:12]}"
    
    async def execute_workflow(self, agents_map: Dict[str, Any]) -> UnderwritingDecision:
        """
        Execute the complete workflow.
        
        Args:
            agents_map: Mapping of agent step to agent instance
            
        Returns:
            UnderwritingDecision: Final underwriting decision
        """
        try:
            # Document intake
            await self._execute_step(
                WorkflowStep.DOCUMENT_INTAKE,
                agents_map.get("document_intake")
            )
            
            # Parallel verification
            await self._execute_parallel_step(
                WorkflowStep.PARALLEL_VERIFICATION,
                agents_map
            )
            
            # Risk assessment
            await self._execute_step(
                WorkflowStep.RISK_ASSESSMENT,
                agents_map.get("risk_assessment")
            )
            
            # Final decision
            await self._execute_step(
                WorkflowStep.FINAL_DECISION,
                agents_map.get("final_approval")
            )
            
            # Check if human review is needed
            final_decision = self.agent_results.get("final_approval", {})
            if final_decision.get("human_review_required"):
                self._transition_to(WorkflowStep.HUMAN_REVIEW)
                # In real system, this would wait for human review
            else:
                self._transition_to(WorkflowStep.COMPLETED)
                self.state.status = "COMPLETED"
            
            # Create final decision record
            decision = await self._create_decision_record(final_decision)
            
            return decision
            
        except Exception as e:
            self.state.status = "FAILED"
            self.state.last_error = str(e)
            self._transition_to(WorkflowStep.FAILED)
            raise
    
    async def _execute_step(
        self,
        step: WorkflowStep,
        agent: Any
    ) -> None:
        """Execute a single workflow step."""
        self._transition_to(step)
        
        # Prepare input for agent
        agent_input = self._prepare_agent_input(step)
        
        # Run agent
        result = await agent.run(**agent_input)
        
        # Store result
        self.agent_results[step.value] = result
        
        # Generate evidence
        evidence = agent.generate_evidence(result)
        self.evidence_log.add_evidence(evidence)
        
        # Create checkpoint
        self._create_checkpoint()
        
        self.state.completed_agents.append(agent.agent_name)
    
    async def _execute_parallel_step(
        self,
        step: WorkflowStep,
        agents_map: Dict[str, Any]
    ) -> None:
        """Execute parallel agents."""
        self._transition_to(step)
        
        parallel_agents = ParallelAgents.get_parallel_agents(step)
        
        # Get agent instances for parallel execution
        tasks = []
        agent_keys = []
        
        for parallel_step in parallel_agents:
            agent_key = parallel_step.value.replace("_", "_").lower()
            agent = agents_map.get(agent_key)
            
            if agent:
                agent_input = self._prepare_agent_input(parallel_step)
                tasks.append(agent.run(**agent_input))
                agent_keys.append(parallel_step.value)
        
        # Run agents concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.state.last_error = str(result)
                raise result
            
            agent_key = agent_keys[i]
            self.agent_results[agent_key] = result
            self.state.completed_agents.append(agent_key)
            
            # Note: In real implementation, would generate evidence here
        
        self._create_checkpoint()
    
    def _prepare_agent_input(self, step: WorkflowStep) -> Dict[str, Any]:
        """Prepare input for an agent."""
        base_input = {
            "application_id": self.application_id,
            "applicant_id": self.applicant_data.get("applicant_id"),
        }
        
        # Add step-specific inputs
        if step == WorkflowStep.DOCUMENT_INTAKE:
            base_input.update({
                "documents_content": {}  # In real system, would load actual documents
            })
        
        elif step == WorkflowStep.INCOME_VERIFICATION:
            base_input.update({
                "stated_income": self.applicant_data.get("applicant_income", 0),
                "employment_status": self.applicant_data.get("employment_status", "FULL_TIME"),
                "employment_length_months": self.applicant_data.get("employment_length_months", 0),
                "paystub_data": self.agent_results.get("extracted_fields", {}).get("paystub", {}),
                "bank_statement_data": self.agent_results.get("extracted_fields", {}).get("bank", {})
            })
        
        elif step == WorkflowStep.CREDIT_SCORING:
            base_input.update({
                "credit_score": self.applicant_data.get("credit_score"),
                "loan_amount": self.applicant_data.get("loan_amount", 0),
                "loan_purpose": self.applicant_data.get("loan_purpose", "")
            })
        
        elif step == WorkflowStep.FRAUD_DETECTION:
            base_input.update({
                "applicant_email": self.applicant_data.get("applicant_email", ""),
                "applicant_phone": self.applicant_data.get("applicant_phone", ""),
                "fraud_signals": self.applicant_data.get("fraud_signals", {})
            })
        
        elif step == WorkflowStep.COMPLIANCE_CHECK:
            base_input.update({
                "applicant_first_name": self.applicant_data.get("applicant_first_name", ""),
                "applicant_last_name": self.applicant_data.get("applicant_last_name", ""),
                "applicant_email": self.applicant_data.get("applicant_email", ""),
                "loan_amount": self.applicant_data.get("loan_amount", 0)
            })
        
        elif step == WorkflowStep.RISK_ASSESSMENT:
            base_input.update({
                "applicant_income": self.applicant_data.get("applicant_income", 0),
                "loan_amount": self.applicant_data.get("loan_amount", 0),
                "debt_to_income_ratio": self.applicant_data.get("debt_to_income_ratio", 0),
                "credit_score": self.applicant_data.get("credit_score", 650),
                "employment_status": self.applicant_data.get("employment_status", "FULL_TIME"),
                "income_verification_result": self.agent_results.get("INCOME_VERIFICATION", {}),
                "credit_scoring_result": self.agent_results.get("CREDIT_SCORING", {}),
                "fraud_detection_result": self.agent_results.get("FRAUD_DETECTION", {}),
                "compliance_result": self.agent_results.get("COMPLIANCE_CHECK", {})
            })
        
        elif step == WorkflowStep.FINAL_DECISION:
            base_input.update({
                "applicant_income": self.applicant_data.get("applicant_income", 0),
                "loan_amount": self.applicant_data.get("loan_amount", 0),
                "risk_assessment_result": self.agent_results.get("RISK_ASSESSMENT", {})
            })
        
        return base_input
    
    def _transition_to(self, step: WorkflowStep) -> None:
        """Transition to a new workflow step."""
        if not StateTransitionMap.is_valid_transition(
            self._step_enum_to_status(self.state.current_step),
            step
        ):
            raise ValueError(f"Invalid transition: {self.state.current_step} -> {step}")
        
        self.state.current_step = self._step_enum_to_status(step)
        self.state.updated_at = datetime.utcnow()
        self.state.state_version += 1
    
    def _create_checkpoint(self) -> None:
        """Create workflow checkpoint for recovery."""
        checkpoint = WorkflowCheckpoint(
            workflow_id=self.workflow_id,
            application_id=self.application_id,
            current_step=self.state.current_step,
            state_snapshot=self.state.dict(),
            completed_agents_output=self.agent_results.copy(),
            checkpoint_hash=self._compute_state_hash()
        )
        self.checkpoint_history.append(checkpoint)
    
    def _compute_state_hash(self) -> str:
        """Compute SHA256 hash of current state."""
        import hashlib
        state_json = json.dumps(self.agent_results, sort_keys=True, default=str)
        return hashlib.sha256(state_json.encode()).hexdigest()
    
    async def _create_decision_record(self, final_decision: Dict[str, Any]) -> UnderwritingDecision:
        """Create final decision record."""
        decision = UnderwritingDecision(
            application_id=self.application_id,
            decision=ApprovalDecision(final_decision.get("decision", "ESCALATE_TO_HUMAN")),
            risk_level=RiskLevel(final_decision.get("risk_level", "MEDIUM")),
            approval_confidence=final_decision.get("approval_confidence", 0.5),
            reason_codes=final_decision.get("reason_codes", []),
            detailed_explanation=self._generate_explanation(final_decision),
            agent_evidence=self.agent_results,
            trace_id=self.trace_id,
            workflow_id=self.workflow_id,
            human_review_required=final_decision.get("human_review_required", False),
            escalation_reason=final_decision.get("escalation_reason")
        )
        return decision
    
    def _generate_explanation(self, final_decision: Dict[str, Any]) -> str:
        """Generate human-readable explanation of decision."""
        decision = final_decision.get("decision", "ESCALATE_TO_HUMAN")
        reasons = final_decision.get("reason_codes", [])
        
        explanation = f"Underwriting decision: {decision}. "
        explanation += f"Key factors: {', '.join(reasons[:3])}. "
        
        risk_factors = self.agent_results.get("RISK_ASSESSMENT", {}).get("risk_factors", {})
        if risk_factors:
            explanation += f"Risk assessment: {json.dumps(risk_factors, default=str)}"
        
        return explanation
    
    def _step_enum_to_status(self, step) -> WorkflowStep:
        """Convert to WorkflowStep enum if needed."""
        if isinstance(step, str):
            return WorkflowStep[step]
        return step
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get workflow execution summary."""
        return {
            "workflow_id": self.workflow_id,
            "application_id": self.application_id,
            "trace_id": self.trace_id,
            "current_step": self.state.current_step,
            "status": self.state.status,
            "completed_agents": self.state.completed_agents,
            "evidence_items_count": len(self.evidence_log.evidence_items),
            "duration_seconds": (self.state.updated_at - self.state.created_at).total_seconds(),
            "agent_results_summary": {
                k: {
                    "confidence": v.get("confidence", 0),
                    "status": v.get("verification_status") or v.get("decision", "N/A")
                }
                for k, v in self.agent_results.items()
            }
        }
