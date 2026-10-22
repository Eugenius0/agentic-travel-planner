import pytest
from pydantic import ValidationError

from app.schemas import Activity


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
