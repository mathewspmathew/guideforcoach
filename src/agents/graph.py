from langgraph.graph import StateGraph, END, START
# from src.agents.state import AgentState
from src.agents.state import AgentState

from src.agents.nodes import scout_node, researcher_node, director_node

def build_app():
    # 1. Initialize Graph
    workflow = StateGraph(AgentState)

    # 2. Add Nodes
    workflow.add_node("scout", scout_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("director", director_node)

    # 3. Define Edges (The Flow)
    # Start -> Scout -> Researcher -> Director -> End
    # workflow.set_entry_point("scout")
    workflow.add_edge(START,"scout")
    workflow.add_edge("scout", "researcher")
    workflow.add_edge("researcher", "director")
    workflow.add_edge("director", END)

    # 4. Compile
    app = workflow.compile()
    return app