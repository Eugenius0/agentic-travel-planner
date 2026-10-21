from fastapi import FastAPI

from app.schemas import TravelItinerary, TravelRequest
from app.llm import generate_itinerary

app = FastAPI(
    title="Agentic Travel Planner API",
    description="AI-powered travel planning using LangGraph and MCP",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/trips/plan", response_model=TravelItinerary)
def plan_trip(request: TravelRequest):
    return generate_itinerary(request)
