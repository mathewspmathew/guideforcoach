"""
Router: /agent
Exposes endpoints to run the LangGraph scouting agent for a given player.

Features:
  - Rate limiting    : 5 requests/minute per IP  (via slowapi)
  - Player validation: rejects unknown names before touching the LLM
  - Response caching : returns cached results instantly on repeated queries
"""
from fastapi import APIRouter, HTTPException, Request
from pathlib import Path
import re
from datetime import datetime

from src.agents.graph import build_app
from resultfilecreate import create_file
from api.schemas import AgentRequest, AgentResponse
from api.cache import get_cached, set_cached
from api.validators import is_known_player
from api.main import limiter

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/scout", response_model=AgentResponse, summary="Run the scouting agent for a player")
@limiter.limit("5/minute")
def scout_player(request: Request, body: AgentRequest):
    """
    Runs the full LangGraph agent workflow for the given player.

    **Rate limit**: 5 requests per minute per IP address.

    **Flow**:
    1. Return cached result immediately if the player was already scouted.
    2. Validate the name against the local dataset — returns 404 for unknown names.
    3. Run the LangGraph pipeline (Scout → Researcher → Director nodes).
    4. Cache and return the result.

    The report is also saved as a Markdown file inside the `reports/` folder.
    """
    player_name = body.player_name.strip()
    if not player_name:
        raise HTTPException(status_code=422, detail="player_name must not be empty.")

    #Cache hit — return instantly, no LLM call
    cached = get_cached(player_name)
    if cached:
        return AgentResponse(**cached, cached=True)

    #Validate player name against dataset
    if not is_known_player(player_name):
        raise HTTPException(
            status_code=404,
            detail=(
                f"'{player_name}' was not found in our player dataset. "
                "Please check the spelling or try a different name."
            ),
        )

    # Run LangGraph agent
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

        result = {
            "target_player": target_player,
            "final_report": final_report,
            "report_file": report_file,
        }

        # Store in cache for future requests
        set_cached(player_name, result)

        return AgentResponse(**result, cached=False)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
