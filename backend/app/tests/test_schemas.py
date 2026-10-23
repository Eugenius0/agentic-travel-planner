import pytest
from pydantic import ValidationError

from app.schemas import Activity, TravelItinerary, TripCostBreakdown


def test_activity_accepts_source_url():
    activity = Activity(
        name="Vasa Museum",
        description="Visit the maritime museum.",
        estimated_cost=20,
        source_url="https://www.vasamuseet.se",
    )

    assert str(activity.source_url) == "https://www.vasamuseet.se/"


def test_activity_allows_missing_source_url():
    activity = Activity(
        name="City walk",
        description="Explore Stockholm.",
        estimated_cost=0,
    )

    assert activity.source_url is None


def test_activity_rejects_invalid_source_url():
    with pytest.raises(ValidationError):
        Activity(
            name="Museum",
            description="Visit a museum.",
            estimated_cost=20,
            source_url="not-a-valid-url",
        )


def test_trip_cost_breakdown_total():
    breakdown = TripCostBreakdown(
        transportation=420,
        accommodation=360,
        food=210,
        activities=180,
        local_transportation=70,
    )

    assert breakdown.total == 1240


def test_itinerary_defaults_to_activity_scope():
    itinerary = TravelItinerary(
        destination="Rome",
        currency="EUR",
        days=[],
        total_estimated_cost=180,
    )

    assert itinerary.budget_scope == "activities"
    assert itinerary.cost_breakdown is None
