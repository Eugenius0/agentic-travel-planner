from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.graph import build_travel_graph
from app.schemas import TravelItinerary, TravelRequest

app = FastAPI(
    title="Agentic Travel Planner API",
    description="AI-powered travel planning using LangGraph and MCP",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

travel_graph = build_travel_graph()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/trips/plan", response_model=TravelItinerary)
async def plan_trip(request: TravelRequest):
    result = await travel_graph.ainvoke(
        {
            "request": request,
            "research_results": "",
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
