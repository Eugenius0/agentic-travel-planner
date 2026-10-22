from pydantic import BaseModel, Field, HttpUrl


class TravelRequest(BaseModel):
    destination: str = Field(
        min_length=2,
        description="Destination city or region",
        examples=["Tokyo, Japan"],
    )

    duration_days: int = Field(
        ge=1,
        le=30,
        description="Number of days for the trip",
        examples=[7],
    )

    budget: float = Field(
        gt=0,
        description="Total travel budget",
        examples=[1500],
    )

    currency: str = Field(
        default="EUR",
        min_length=3,
        max_length=3,
        description="Three-letter currency code",
        examples=["EUR"],
    )

    interests: list[str] = Field(
        min_length=1,
        description="Traveler interests",
        examples=[["Nature", "Food", "Culture"]],
    )


class Activity(BaseModel):
    name: str
    description: str
    estimated_cost: float = Field(ge=0)
    source_url: HttpUrl | None = None


class DayPlan(BaseModel):
    day: int = Field(ge=1, description="Day number of the trip")
    activities: list[Activity] = Field(
        min_length=1, description="Activities planned for this day"
    )


class TravelItinerary(BaseModel):
    destination: str
    currency: str
    days: list[DayPlan]
    total_estimated_cost: float = Field(
        ge=0, description="Total estimated cost of all planned activities"
    )
