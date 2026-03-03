"""
Pydantic models for request and response bodies.
"""
from pydantic import BaseModel


# pipeline response model - basically in this schema pipeline is going to return

class PipelineRunResponse(BaseModel):
    status: str
    message: str



class AgentRequest(BaseModel):
    player_name: str

# schema for response model of agent router - in /scout
class AgentResponse(BaseModel):
    target_player: str
    final_report: str
    report_file: str           # relative path to the saved .md file in reports/
    cached: bool = False       # True when result was served from in-memory cache