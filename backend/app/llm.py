import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from app.schemas import TravelItinerary, TravelRequest


def create_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not configured")

    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=0.3,
        max_retries=0,
        timeout=30,
    )


def generate_itinerary(
    request: TravelRequest,
    research_results: str = "",
) -> TravelItinerary:
    llm = create_llm()

    structured_llm = llm.with_structured_output(
        TravelItinerary,
        method="function_calling",
    )

    messages = [
        SystemMessage(
            content=(
                "You are an experienced travel planner. "
                "Create realistic, personalized travel itineraries. "
                "Organize activities by day and consider the traveler's interests. "
                "Estimate activity costs in the requested currency. "
                "Include exactly the requested number of days. "
                "Keep estimated activity costs within the provided budget. "
                "The total_estimated_cost must equal the sum of all activity costs. "
                "Use destination research when available, prioritizing reliable sources. "
                "Do not invent admission prices or opening hours. "
                "Treat prices as estimates unless clearly confirmed by a source. "
                "Do not claim that estimated prices are verified or live."
            )
        ),
        HumanMessage(
            content=(
                f"Destination: {request.destination}\n"
                f"Duration: {request.duration_days} days\n"
                f"Budget: {request.budget} {request.currency}\n"
                f"Interests: {', '.join(request.interests)}\n\n"
                f"Destination research from web sources:\n"
                f"{research_results if research_results else 'No research available.'}\n\n"
                "Use this research to select relevant attractions and activities. "
                "Prefer researched information over general knowledge. "
                "Do not invent admission prices or opening hours."
            )
        ),
    ]

    return structured_llm.invoke(messages)
