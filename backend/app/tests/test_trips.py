from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_plan_trip_valid_request():
    payload = {
        "destination": "Tokyo, Japan",
        "duration_days": 7,
        "budget": 1500,
        "currency": "EUR",
        "interests": ["Nature", "Food", "Culture"],
    }

    response = client.post("/api/trips/plan", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Travel request received successfully",
        "travel_request": payload,
    }


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
