from typing import TypedDict

from app.schemas import TravelItinerary, TravelRequest
from app.llm import generate_itinerary
from langgraph.graph import StateGraph, START, END
from app.research_agent import run_research_agent


class TravelState(TypedDict):
    request: TravelRequest
    research_results: str
    itinerary: TravelItinerary | None
    validation_errors: list[str]
    retry_count: int


async def research_destination_node(state: TravelState) -> dict:
    request = state["request"]

    research_results = await run_research_agent(
        destination=request.destination,
        interests=request.interests,
    )

    return {"research_results": research_results}


def generate_itinerary_node(state: TravelState) -> dict:
    itinerary = generate_itinerary(
        state["request"],
        state["research_results"],
    )

    return {
        "itinerary": itinerary,
        "validation_errors": [],
        "retry_count": state["retry_count"] + 1,
    }


def validate_itinerary_node(state: TravelState) -> dict:
    request = state["request"]
    itinerary = state["itinerary"]
    errors = []

    if itinerary is None:
        return {"validation_errors": ["No itinerary was generated."]}

    if len(itinerary.days) != request.duration_days:
        errors.append(
            f"Expected {request.duration_days} days, "
            f"but received {len(itinerary.days)}."
        )

    expected_days = list(range(1, request.duration_days + 1))
    actual_days = [day.day for day in itinerary.days]

    if actual_days != expected_days:
        errors.append("Day numbers are incorrect or out of order.")

    if itinerary.currency.upper() != request.currency.upper():
        errors.append("Itinerary currency does not match the request.")

    actual_total = sum(
        activity.estimated_cost for day in itinerary.days for activity in day.activities
    )

    if abs(actual_total - itinerary.total_estimated_cost) > 0.01:
        errors.append(
            f"Reported total {itinerary.total_estimated_cost} "
            f"does not match calculated total {actual_total:.2f}."
        )

    if actual_total > request.budget:
        errors.append(
            f"Estimated cost {actual_total:.2f} exceeds "
            f"budget {request.budget:.2f}."
        )

    return {"validation_errors": errors}


MAX_GENERATION_ATTEMPTS = 3


def route_after_validation(state: TravelState) -> str:
    if not state["validation_errors"]:
        return "complete"

    if state["retry_count"] < MAX_GENERATION_ATTEMPTS:
        return "retry"

    return "failed"


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("research", research_destination_node)
    graph.add_node("generate", generate_itinerary_node)
    graph.add_node("validate", validate_itinerary_node)

    graph.add_edge(START, "research")
    graph.add_edge("research", "generate")
    graph.add_edge("generate", "validate")

    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "complete": END,
            "retry": "generate",
            "failed": END,
        },
    )

    return graph.compile()
