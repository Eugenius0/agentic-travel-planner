from unittest.mock import patch

from app.graph import build_travel_graph
from app.schemas import TravelItinerary, TravelRequest


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
    return build_travel_graph().invoke(
        {
            "request": make_request(),
            "itinerary": None,
            "validation_errors": [],
            "retry_count": 0,
        }
    )


def test_valid_itinerary_first_attempt():
    with patch(
        "app.graph.generate_itinerary",
        return_value=make_itinerary(50),
    ) as mock_generate:
        result = run_graph()

    assert result["validation_errors"] == []
    assert result["retry_count"] == 1
    mock_generate.assert_called_once()


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
