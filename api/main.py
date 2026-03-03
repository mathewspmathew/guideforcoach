"""
Mount all routers here and configure app metadata.
"""
from fastapi import FastAPI
from api.routers import pipeline, agent

app = FastAPI(
    title="GuideForCoach API",
    description=(
        "HTTP interface for the Moneyball scouting system.\n"
        "/pipeline — trigger ML data pipeline & model training\n"
        "/agent — run the LangGraph scouting agent for a player"
    )
)

# we have each router for ml pipeline and agents
app.include_router(pipeline.router)
app.include_router(agent.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message":"Welcome to coach dashboard"}