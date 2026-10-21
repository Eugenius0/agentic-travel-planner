from fastapi import FastAPI

from app.schemas import TravelRequest

app = FastAPI(
    title="Agentic Travel Planner API",
    description="AI-powered travel planning using LangGraph and MCP",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/trips/plan")
def plan_trip(request: TravelRequest):
    return {
        "message": "Travel request received successfully",
        "travel_request": request.model_dump(),
    }
