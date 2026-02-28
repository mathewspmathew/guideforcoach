from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from src.model import SimilarityEngine
from src.agents.state import AgentState
from src.config import RAW_DATA_PATH # Ensure paths are loaded
from dotenv import load_dotenv
import os

load_dotenv()


# Initialize Tools
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)
search_tool = TavilySearch(max_results=2)
ml_engine = SimilarityEngine()

# --- NODE 1: THE SCOUT (Uses your ML Code) ---
def scout_node(state: AgentState):
    print(f"\n🕵️  SCOUT: Looking for players similar to {state['target_player']}...")

    # 1. Load Data/Model (Lazy loading handled in class)
    # We assume model is already trained via main_pipeline.py
    # If not, it will try to load from disk
    result = ml_engine.inference(state['target_player'])

    if "error" in result:
        # Fallback if player not found
        return {"similar_players": [], "market_research": f"Error: {result['error']}"}

    # 2. Return the list of matches to the State
    return {"similar_players": result['recommendations']}

# --- NODE 2: THE RESEARCHER (Uses Web Search) ---
def researcher_node(state: AgentState):
    players = state['similar_players']
    if not players:
        return {"market_research": "No players found to research."}
    else:
        print(f"\n🔎 RESEARCHER: Checking market data for {len(players)} players...")

        research_summary = ""

        for player in players:
            name = player['name']
            team = player['squad']
            query = f"{name} {team} transfer market value injury history news 2024"

            try:
                # 1. Call the tool
                search_results = search_tool.invoke(query)

                # 2. Extract snippets from the 'results' key
                # Modern TavilySearch returns: {"results": [{"content": "...", ...}, ...]}
                if "results" in search_results:
                    snippets = "\n".join([res.get('content', '') for res in search_results['results']])
                    research_summary += f"--- {name} ({team}) ---\n{snippets}\n\n"
                else:
                    research_summary += f"No results found for {name}.\n"

            except Exception as e:
                # Print the actual error to your console for debugging
                print(f"Error researching {name}: {e}")
                research_summary += f"Could not find data for {name}.\n"


        return {"market_research": research_summary}

# --- NODE 3: THE DIRECTOR (Uses LLM) ---
def director_node(state: AgentState):
    print("\n👔 DIRECTOR: Writing final report...")

    # Define the Prompt
    template = """You are the Sporting Director of a top football club.

    GOAL: Write a scouting report recommending a replacement for: {target}

    DATA FROM SCOUT (Statistical Match):
    {stats}

    DATA FROM RESEARCHER (Market/News):
    {market}

    INSTRUCTIONS:
    1. Compare the options based on Stats AND Market feasibility.
    2. Be professional, concise, and decisive.
    3. Recommend ONE primary target and ONE backup.

    FORMAT:
    ## Executive Summary
    ## Player Analysis
    ## Final Recommendation
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    # Run the LLM
    response = chain.invoke({
        "target": state['target_player'],
        "stats": state['similar_players'],
        "market": state['market_research']
    })

    return {"final_report": response.content}