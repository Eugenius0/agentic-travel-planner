from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import TravelItinerary

client = TestClient(app)


def test_plan_trip_valid_request():
    payload = {
        "destination": "Stockholm, Sweden",
        "duration_days": 2,
        "budget": 150,
        "currency": "EUR",
        "interests": ["Nature", "Museums"],
    }

    mock_itinerary = TravelItinerary(
        destination="Stockholm, Sweden",
        currency="EUR",
        days=[
            {
                "day": 1,
                "activities": [
                    {
                        "name": "Vasa Museum",
                        "description": "Visit the historic warship museum.",
                        "estimated_cost": 20,
                    }
                ],
            },
            {
                "day": 2,
                "activities": [
                    {
                        "name": "Djurgården",
                        "description": "Explore Stockholm's green spaces.",
                        "estimated_cost": 0,
                    }
                ],
            },
        ],
        total_estimated_cost=20,
    )

    with patch(
        "app.main.travel_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={
            "itinerary": mock_itinerary,
            "validation_errors": [],
            "retry_count": 1,
        },
    ) as mock_ainvoke:
        response = client.post("/api/trips/plan", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_itinerary.model_dump()

    mock_ainvoke.assert_awaited_once()

    initial_state = mock_ainvoke.await_args.args[0]
    assert initial_state["request"].destination == "Stockholm, Sweden"
    assert initial_state["research_results"] == ""
    assert initial_state["retry_count"] == 0


def test_plan_trip_negative_budget():
    payload = {
        "destination": "Tokyo, Japan",
        "duration_days": 7,
        "budget": -100,
        "currency": "EUR",
        "interests": ["Nature"],
    }

    response = client.post("/api/trips/plan", json=payload)

    assert response.status_code == 422


def test_plan_trip_empty_interests():
    payload = {
        "destination": "Tokyo, Japan",
        "duration_days": 7,
        "budget": 1500,
        "currency": "EUR",
        "interests": [],
    }

    response = client.post("/api/trips/plan", json=payload)

    assert response.status_code == 422


def test_plan_trip_validation_failure():
    payload = {
        "destination": "Stockholm, Sweden",
        "duration_days": 2,
        "budget": 150,
        "currency": "EUR",
        "interests": ["Nature", "Museums"],
    }

    with patch(
        "app.main.travel_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={
            "itinerary": None,
            "validation_errors": ["Estimated cost exceeds budget."],
            "retry_count": 3,
        },
    ) as mock_ainvoke:
        response = client.post("/api/trips/plan", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"]["message"] == (
        "Could not generate a valid itinerary."
    )
    assert response.json()["detail"]["errors"] == ["Estimated cost exceeds budget."]

    mock_ainvoke.assert_awaited_once()
