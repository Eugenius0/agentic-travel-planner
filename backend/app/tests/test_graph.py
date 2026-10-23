import asyncio
import json
from unittest.mock import patch

from app.graph import build_travel_graph
from app.schemas import TravelItinerary, TravelRequest

MOCK_RESEARCH = json.dumps(
    [
        {
            "title": "Vasa Museum",
            "url": "https://www.vasamuseet.se/en",
            "content": "A museum in Stockholm featuring a historic warship.",
        }
    ]
)


def make_request():
    return TravelRequest(
        destination="Stockholm, Sweden",
        duration_days=1,
        budget=100,
        currency="EUR",
        interests=["Museums"],
    )


def make_itinerary(cost):
    return TravelItinerary(
        destination="Stockholm, Sweden",
        currency="EUR",
        days=[
            {
                "day": 1,
                "activities": [
                    {
                        "name": "Vasa Museum",
                        "description": "Visit the historic warship museum.",
                        "estimated_cost": cost,
                    }
                ],
            }
        ],
        total_estimated_cost=cost,
    )


def run_graph():
    async def mock_research(state):
        return {"research_results": MOCK_RESEARCH}

    async def execute():
        # Mock research before compiling the graph.
        with patch(
            "app.graph.research_destination_node",
            new=mock_research,
        ):
            graph = build_travel_graph()

        return await graph.ainvoke(
            {
                "request": make_request(),
                "research_results": "",
                "itinerary": None,
                "validation_errors": [],
                "retry_count": 0,
            }
        )

    return asyncio.run(execute())


def test_valid_itinerary_first_attempt():
    with patch(
        "app.graph.generate_itinerary",
        return_value=make_itinerary(50),
    ) as mock_generate:
        result = run_graph()

    assert result["validation_errors"] == []
    assert result["retry_count"] == 1
    assert result["research_results"] == MOCK_RESEARCH

    mock_generate.assert_called_once_with(
        make_request(),
        MOCK_RESEARCH,
    )


def test_invalid_itinerary_then_successful_retry():
    with patch(
        "app.graph.generate_itinerary",
        side_effect=[
            make_itinerary(150),
            make_itinerary(50),
        ],
    ) as mock_generate:
        result = run_graph()

    assert result["validation_errors"] == []
    assert result["retry_count"] == 2
    assert result["itinerary"].total_estimated_cost == 50
    assert mock_generate.call_count == 2
    assert result["research_results"] == MOCK_RESEARCH


def test_invalid_itinerary_exhausts_retries():
    with patch(
        "app.graph.generate_itinerary",
        return_value=make_itinerary(150),
    ) as mock_generate:
        result = run_graph()

    assert result["retry_count"] == 3
    assert result["validation_errors"]
    assert result["itinerary"].total_estimated_cost == 150
    assert mock_generate.call_count == 3
    assert result["research_results"] == MOCK_RESEARCH


def test_research_node_uses_autonomous_agent():
    import asyncio
    from unittest.mock import AsyncMock, patch

    from app.graph import research_destination_node
    from app.schemas import TravelRequest

    request = TravelRequest(
        destination="Stockholm",
        duration_days=2,
        budget=150,
        currency="EUR",
        interests=["Nature", "Museums"],
    )

    mock_research = (
        "Vasa Museum: maritime museum in Stockholm. "
        "Source: https://www.vasamuseet.se"
    )

    async def run_test():
        with patch(
            "app.graph.run_research_agent",
            new_callable=AsyncMock,
            return_value=mock_research,
        ) as mocked_agent:
            result = await research_destination_node(
                {
                    "request": request,
                }
            )

            mocked_agent.assert_awaited_once_with(
                destination="Stockholm",
                interests=["Nature", "Museums"],
            )

            assert result["research_results"] == mock_research

    asyncio.run(run_test())


def test_validator_rejects_incorrect_total_cost():
    from app.graph import validate_itinerary_node
    from app.schemas import (
        Activity,
        DayPlan,
        TravelItinerary,
        TravelRequest,
    )

    request = TravelRequest(
        destination="Stockholm",
        duration_days=1,
        budget=100,
        currency="EUR",
        interests=["Museums"],
    )

    itinerary = TravelItinerary(
        destination="Stockholm",
        currency="EUR",
        days=[
            DayPlan(
                day=1,
                activities=[
                    Activity(
                        name="Museum visit",
                        description="Explore a museum.",
                        estimated_cost=25,
                    ),
                    Activity(
                        name="Guided tour",
                        description="Explore the city.",
                        estimated_cost=30,
                    ),
                ],
            )
        ],
        total_estimated_cost=40,
    )

    result = validate_itinerary_node(
        {
            "request": request,
            "itinerary": itinerary,
            "validation_errors": [],
            "retry_count": 1,
            "research_results": "",
        }
    )

    assert result["validation_errors"]
    assert any("total" in error.lower() for error in result["validation_errors"])


def test_validator_rejects_full_trip_over_budget():
    from app.graph import validate_itinerary_node
    from app.schemas import (
        Activity,
        DayPlan,
        TravelItinerary,
        TravelRequest,
        TripCostBreakdown,
    )

    request = TravelRequest(
        destination="Rome",
        duration_days=1,
        budget=500,
        currency="EUR",
        interests=["Culture"],
    )

    itinerary = TravelItinerary(
        destination="Rome",
        currency="EUR",
        days=[
            DayPlan(
                day=1,
                activities=[
                    Activity(
                        name="Colosseum",
                        description="Explore ancient Rome.",
                        estimated_cost=25,
                    )
                ],
            )
        ],
        total_estimated_cost=25,
        cost_breakdown=TripCostBreakdown(
            transportation=200,
            accommodation=300,
            food=100,
            activities=25,
            local_transportation=30,
        ),
    )

    result = validate_itinerary_node(
        {
            "request": request,
            "itinerary": itinerary,
            "validation_errors": [],
            "retry_count": 1,
            "research_results": "",
        }
    )

    assert any(
        "total trip cost" in error.lower() for error in result["validation_errors"]
    )


def test_validator_rejects_mismatched_activity_subtotal():
    from app.graph import validate_itinerary_node
    from app.schemas import (
        Activity,
        DayPlan,
        TravelItinerary,
        TravelRequest,
        TripCostBreakdown,
    )

    request = TravelRequest(
        destination="Rome",
        duration_days=1,
        budget=1000,
        currency="EUR",
        interests=["Culture"],
    )

    itinerary = TravelItinerary(
        destination="Rome",
        currency="EUR",
        days=[
            DayPlan(
                day=1,
                activities=[
                    Activity(
                        name="Colosseum",
                        description="Explore ancient Rome.",
                        estimated_cost=25,
                    )
                ],
            )
        ],
        total_estimated_cost=25,
        cost_breakdown=TripCostBreakdown(
            transportation=200,
            accommodation=300,
            food=100,
            activities=50,  # Incorrect: actual activity cost is 25
            local_transportation=30,
        ),
    )

    result = validate_itinerary_node(
        {
            "request": request,
            "itinerary": itinerary,
            "validation_errors": [],
            "retry_count": 1,
            "research_results": "",
        }
    )

    assert any(
        "activity costs in the breakdown" in error.lower()
        for error in result["validation_errors"]
    )
