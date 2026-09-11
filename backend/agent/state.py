from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class AgentStep:
    step_index: int
    agent_action: str
    tool_used: str
    tool_input: Dict[str, Any]
    evidence_found: Dict[str, Any]
    decision: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    timestamp: str = ""

@dataclass
class InvestigationState:
    alert_id: str
    goal: str
    status: str = "IN_PROGRESS"  # IN_PROGRESS, COMPLETED, REQUIRES_HUMAN_REVIEW, ADAPTED, RECOVERING
    current_step: int = 0
    evidence: Dict[str, Any] = field(default_factory=dict)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    decision: Optional[str] = None  # ATTACK_SUCCESSFUL, ATTACK_FAILED, FALSE_POSITIVE, INCONCLUSIVE
    confidence: float = 0.0
    risk_score: float = 0.0
    response_recommended: Optional[str] = None
    response_executed: Optional[str] = None
    verification_result: Optional[Dict[str, Any]] = None
    contradiction_detected: bool = False
    recovery_attempted: bool = False
    final_summary: str = ""
