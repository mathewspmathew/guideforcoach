from typing import TypedDict, List

class AgentState(TypedDict):
    target_player: str          # for input: "Declan Rice"
    similar_players: List[dict] # Output from Scout: [{"name": "Rodri", "score": 90}, ...]
    market_research: str        # Output from Researcher: "Rodri is valued at €100m..."
    final_report: str           # Output from Director: "Recommendation: Buy Rodri..."