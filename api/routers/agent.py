"""
Router: /agent
Exposes endpoints to run the LangGraph scouting agent for a given player.
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import re
from datetime import datetime

from src.agents.graph import build_app
from resultfilecreate import create_file
from api.schemas import AgentRequest, AgentResponse

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/scout", response_model=AgentResponse, summary="Run the scouting agent for a player")
def scout_player(request: AgentRequest):
    """
    Runs the full LangGraph agent workflow for the given player:
    - Scout node  → gathers player stats
    - Researcher node → finds replacement candidates
    - Director node → compiles the final scouting report

    The report is also saved as a Markdown file inside the `reports/` folder,
    mirroring the behaviour of the CLI (`main_agent.py`).
    """
    player_name = request.player_name.strip()
    if not player_name:
        raise HTTPException(status_code=422, detail="player_name must not be empty.")

    try:
        app = build_app()
        inputs = {"target_player": player_name}
        final_state = app.invoke(inputs)

        final_report: str = final_state["final_report"]
        target_player: str = final_state["target_player"]

        # Save the MD report to reports/ — same as CLI behaviour
        create_file(final_result=final_report, target_player=target_player)

        # Build the expected file path so we can return it in the response
        safe_name = re.sub(r"[^\w\s-]", "", target_player).strip().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = str(Path("reports") / f"{safe_name}_{timestamp}.md")

        return AgentResponse(
            target_player=target_player,
            final_report=final_report,
            report_file=report_file,
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
