from fastapi import FastAPI

from app.schemas import TravelItinerary, TravelRequest
from fastapi import HTTPException

from app.graph import build_travel_graph

app = FastAPI(
    title="Agentic Travel Planner API",
    description="AI-powered travel planning using LangGraph and MCP",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


travel_graph = build_travel_graph()


@app.post("/api/trips/plan", response_model=TravelItinerary)
def plan_trip(request: TravelRequest):
    result = travel_graph.invoke(
        {
            "request": request,
            "itinerary": None,
            "validation_errors": [],
            "retry_count": 0,
        }
    )

    if result["validation_errors"]:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Could not generate a valid itinerary.",
                "errors": result["validation_errors"],
            },
        )

    return result["itinerary"]
