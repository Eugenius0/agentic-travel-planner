import pytest
from pydantic import ValidationError

from app.schemas import (
    Activity,
    TravelRequest,
    TripCostBreakdown,
    DayPlan,
    TravelItinerary,
)


def test_extended_travel_request():
    request = TravelRequest(
        departure_city="Stockholm",
        destination="Rome",
        start_date="2026-11-10",
        end_date="2026-11-14",
        duration_days=5,
        travelers=2,
        budget=1500,
        currency="EUR",
        interests=["Food", "Culture"],
        travel_style="balanced",
    )

    assert request.departure_city == "Stockholm"
    assert request.travelers == 2
    assert request.travel_style == "balanced"


def test_travel_dates_must_match_duration():
    with pytest.raises(ValidationError):
        TravelRequest(
            destination="Rome",
            start_date="2026-11-10",
            end_date="2026-11-14",
            duration_days=3,
            budget=1500,
            interests=["Culture"],
        )


def test_legacy_request_still_works():
    request = TravelRequest(
        destination="Stockholm",
        duration_days=2,
        budget=150,
        interests=["Museums"],
    )

    assert request.departure_city is None
    assert request.travelers == 1
    assert request.travel_style == "balanced"


def test_trip_cost_breakdown_total():
    costs = TripCostBreakdown(
        transportation=300,
        accommodation=480,
        food=180,
        activities=144,
        local_transportation=96,
    )

    assert costs.total == 1200


def test_itinerary_accepts_full_trip_costs():
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

    assert itinerary.cost_breakdown is not None
    assert itinerary.cost_breakdown.total == 655


def test_legacy_itinerary_without_cost_breakdown():
    itinerary = TravelItinerary(
        destination="Stockholm",
        currency="EUR",
        days=[
            DayPlan(
                day=1,
                activities=[
                    Activity(
                        name="City walk",
                        description="Explore Stockholm.",
                        estimated_cost=0,
                    )
                ],
            )
        ],
        total_estimated_cost=0,
    )

    assert itinerary.cost_breakdown is None
