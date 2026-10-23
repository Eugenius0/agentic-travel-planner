import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from app.schemas import TravelItinerary, TravelRequest


def create_llm(max_tokens: int = 700) -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not configured")

    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=0,
        max_tokens=max_tokens,
        max_retries=3,
        timeout=30,
    )


def generate_itinerary(
    request: TravelRequest,
    research_results: str = "",
    validation_errors: list[str] | None = None,
) -> TravelItinerary:
    llm = create_llm()

    structured_llm = llm.with_structured_output(
        TravelItinerary,
        method="function_calling",
    )

    messages = [
        SystemMessage(
            content=(
                "You are an experienced travel planner specializing in "
                "personalized itineraries and realistic trip budgeting. "
                "Create an itinerary containing exactly the requested number "
                "of days, with relevant activities organized by day. "
                "Consider the departure city, destination, dates, traveler "
                "count, interests, and travel style. "
                "Produce a COMPLETE estimated trip budget in the requested "
                "currency for ALL travelers combined. "
                "Always populate cost_breakdown with five non-negative "
                "categories: transportation, accommodation, food, "
                "activities, and local_transportation. "
                "Transportation covers round-trip travel between the "
                "departure city and destination for all travelers. "
                "Accommodation covers the entire stay for the group. "
                "Food covers meals and drinks for all travelers throughout "
                "the trip. "
                "Activities covers all listed itinerary activities. "
                "Local transportation covers travel within the destination. "
                "Set budget_scope to 'full_trip'. "
                "The total_estimated_cost field represents ONLY the sum "
                "of the estimated_cost values of all listed activities. "
                "Set cost_breakdown.activities equal to that same sum. "
                "The complete estimated trip cost is the sum of the five "
                "cost_breakdown categories. "
                "Try to keep the complete estimated trip cost within the "
                "user's total budget. Prefer affordable alternatives when "
                "necessary, without inventing implausibly low prices. "
                "Use destination research when available, prioritizing "
                "reliable and relevant sources. "
                "Do not invent admission prices, flight prices, hotel "
                "prices, opening hours, or source URLs. "
                "When reliable price information is unavailable, provide "
                "reasonable approximate estimates and treat them explicitly "
                "as estimates, not verified or live prices. "
                "Include a source_url for an activity only when the URL "
                "appears in the provided research and supports that "
                "specific activity. Otherwise set source_url to null. "
                "Return a complete, internally consistent itinerary "
                "matching the required structured output schema."
            )
        ),
        HumanMessage(
            content=(
                f"Departure city: {request.departure_city or 'Not specified'}\n"
                f"Destination: {request.destination}\n"
                f"Start date: {request.start_date or 'Not specified'}\n"
                f"End date: {request.end_date or 'Not specified'}\n"
                f"Duration: {request.duration_days} days\n"
                f"Travelers: {request.travelers}\n"
                f"Travel style: {request.travel_style}\n"
                f"TOTAL trip budget: {request.budget} {request.currency}\n"
                f"Interests: {', '.join(request.interests)}\n\n"
                "Destination research from web sources:\n"
                f"{research_results if research_results else 'No research available.'}\n\n"
                "Generate the itinerary and a complete estimated trip "
                "cost breakdown for the entire group. "
                "Do not treat the total budget as an activities-only budget. "
                "Ensure all activity costs add up correctly."
            )
        ),
    ]
    if validation_errors:
        messages.append(
            HumanMessage(
                content=(
                    "Your previous itinerary failed validation for these reasons:\n"
                    + "\n".join(f"- {error}" for error in validation_errors)
                    + "\n\nGenerate a corrected itinerary. "
                    "Ensure the complete trip cost is within the budget, "
                    "all activity totals match, and all required fields are present. "
                    "Do not invent unrealistically low costs just to pass validation."
                )
            )
        )
    return structured_llm.invoke(messages)
