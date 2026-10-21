from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


from unittest.mock import patch

from app.schemas import TravelItinerary


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
        "app.main.generate_itinerary", return_value=mock_itinerary
    ) as mock_generate:
        response = client.post("/api/trips/plan", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_itinerary.model_dump()

    mock_generate.assert_called_once()


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
