import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import APIConnectionError, APITimeoutError, RateLimitError

from app.graph import build_travel_graph
from app.schemas import TravelItinerary, TravelRequest

load_dotenv()

logger = logging.getLogger(__name__)

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
    try:
        result = await travel_graph.ainvoke(
            {
                "request": request,
                "research_results": "",
                "itinerary": None,
                "validation_errors": [],
                "retry_count": 0,
            }
        )

    except RateLimitError as exc:
        logger.warning("Groq rate limit exceeded: %s", exc)
        raise HTTPException(
            status_code=429,
            detail="The AI service is temporarily busy. Please try again shortly.",
        ) from exc

    except (APITimeoutError, APIConnectionError) as exc:
        logger.warning("AI service connection error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="The AI service is temporarily unavailable. Please try again later.",
        ) from exc

    except Exception as exc:
        logger.exception("Trip generation failed")
        raise HTTPException(
            status_code=500,
            detail="Trip generation failed unexpectedly. Please try again later.",
        ) from exc

    if result["validation_errors"]:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Could not generate a valid itinerary.",
                "errors": result["validation_errors"],
            },
        )

    return result["itinerary"]
