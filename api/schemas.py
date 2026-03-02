"""
Pydantic models for request and response bodies.
"""
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class PipelineRunResponse(BaseModel):
    status: str
    message: str


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class AgentRequest(BaseModel):
    player_name: str


class AgentResponse(BaseModel):
    target_player: str
    final_report: str
    report_file: str  # relative path to the saved .md file in reports/
