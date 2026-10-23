from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.graph import build_travel_graph
from app.schemas import Activity, DayPlan, TravelItinerary, TravelRequest

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

# Temporary development mode. Disable before committing.
USE_MOCK_ITINERARY = True


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/trips/plan", response_model=TravelItinerary)
async def plan_trip(request: TravelRequest):
    if USE_MOCK_ITINERARY:
        mock_activities = [
            (
                "Historic city exploration",
                "Discover the city's iconic landmarks, historic streets, "
                "and beautiful architecture.",
                20.0,
            ),
            (
                "Local food experience",
                "Enjoy authentic local cuisine and explore popular "
                "neighborhood restaurants and markets.",
                35.0,
            ),
            (
                "Cultural discovery",
                "Visit museums, galleries, or cultural attractions "
                "that reflect the destination's history.",
                25.0,
            ),
            (
                "Scenic afternoon walk",
                "Explore picturesque neighborhoods, scenic viewpoints, "
                "and hidden local spots.",
                0.0,
            ),
        ]

        days = [
            DayPlan(
                day=day,
                activities=[
                    Activity(
                        name=name,
                        description=description,
                        estimated_cost=cost,
                        source_url=None,
                    )
                    for name, description, cost in mock_activities
                ],
            )
            for day in range(1, request.duration_days + 1)
        ]

        daily_cost = sum(cost for _, _, cost in mock_activities)

        return TravelItinerary(
            destination=request.destination,
            currency=request.currency,
            days=days,
            total_estimated_cost=daily_cost * request.duration_days,
        )

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
