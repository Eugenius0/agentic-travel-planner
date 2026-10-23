from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.schemas import TravelItinerary, TravelRequest
from app.llm import generate_itinerary
from app.research_agent import run_research_agent

MAX_GENERATION_ATTEMPTS = 3
COST_TOLERANCE = 0.01


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
        validation_errors=state["validation_errors"],
    )

    return {
        "itinerary": itinerary,
        "validation_errors": [],
        "retry_count": state["retry_count"] + 1,
    }


def validate_itinerary_node(state: TravelState) -> dict:
    request = state["request"]
    itinerary = state["itinerary"]
    errors: list[str] = []

    if itinerary is None:
        return {"validation_errors": ["No itinerary was generated."]}

    # Validate itinerary duration and day numbering.
    if len(itinerary.days) != request.duration_days:
        errors.append(
            f"Expected {request.duration_days} days, "
            f"but received {len(itinerary.days)}."
        )

    expected_days = list(range(1, request.duration_days + 1))
    actual_days = [day.day for day in itinerary.days]

    if actual_days != expected_days:
        errors.append("Day numbers are incorrect or out of order.")

    # Validate currency.
    if itinerary.currency.upper() != request.currency.upper():
        errors.append("Itinerary currency does not match the request.")

    # Calculate the actual cost of all planned activities.
    actual_activity_total = round(
        sum(
            activity.estimated_cost
            for day in itinerary.days
            for activity in day.activities
        ),
        2,
    )

    # total_estimated_cost represents activities only.
    if abs(actual_activity_total - itinerary.total_estimated_cost) > COST_TOLERANCE:
        errors.append(
            f"Reported activity total "
            f"{itinerary.total_estimated_cost:.2f} "
            f"does not match calculated activity total "
            f"{actual_activity_total:.2f}."
        )

    # Complete trip budgeting is required for the new workflow.
    if itinerary.budget_scope != "full_trip":
        errors.append("Itinerary must use budget_scope='full_trip'.")

    if itinerary.cost_breakdown is None:
        errors.append("Complete trip cost breakdown is missing.")
    else:
        costs = itinerary.cost_breakdown

        # Ensure the activities category matches the itinerary.
        if abs(costs.activities - actual_activity_total) > COST_TOLERANCE:
            errors.append(
                "Activity costs in the breakdown do not match "
                "the itinerary activity total."
            )

        # Validate the complete trip cost against the user's budget.
        if costs.total > request.budget + COST_TOLERANCE:
            errors.append(
                f"Estimated full trip cost "
                f"{costs.total:.2f} {request.currency} "
                f"exceeds the budget of "
                f"{request.budget:.2f} {request.currency}."
            )

    return {"validation_errors": errors}


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
