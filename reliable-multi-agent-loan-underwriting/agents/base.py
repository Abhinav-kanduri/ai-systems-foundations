"""
Base agent class - abstract parent for all underwriting agents.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional
from schemas.agents import AgentStatus, AgentStateSnapshot


class BaseAgent(ABC):
    """Abstract base agent for loan underwriting workflow."""
    
    def __init__(self, agent_name: str, agent_version: str = "1.0.0"):
        """Initialize agent."""
        self.agent_name = agent_name
        self.agent_version = agent_version
        self.status = AgentStatus.IDLE
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.retry_count = 0
        self.error_message: Optional[str] = None
        self.state_snapshot: Optional[AgentStateSnapshot] = None
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute agent logic.
        
        Must be implemented by subclasses.
        
        Returns:
            dict: Agent output following specified schema
        """
        pass
    
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Run agent with state tracking and error handling.
        
        Args:
            **kwargs: Input parameters for agent
            
        Returns:
            dict: Agent output
            
        Raises:
            Exception: If agent execution fails after retries
        """
        self.start_time = datetime.utcnow()
        self.status = AgentStatus.RUNNING
        
        try:
            result = await self.execute(**kwargs)
            self.status = AgentStatus.COMPLETED
            self.end_time = datetime.utcnow()
            return result
        except Exception as e:
            self.status = AgentStatus.FAILED
            self.error_message = str(e)
            self.end_time = datetime.utcnow()
            raise
    
    def get_state_snapshot(self) -> AgentStateSnapshot:
        """Get current state snapshot."""
        duration_ms = None
        if self.start_time and self.end_time:
            duration_ms = int((self.end_time - self.start_time).total_seconds() * 1000)
        
        return AgentStateSnapshot(
            agent_name=self.agent_name,
            agent_version=self.agent_version,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            duration_ms=duration_ms,
            retry_count=self.retry_count,
            error_message=self.error_message
        )
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> bool:
        """Validate required input fields."""
        for field in required_fields:
            if field not in input_data or input_data[field] is None:
                raise ValueError(f"Missing required field: {field}")
        return True
