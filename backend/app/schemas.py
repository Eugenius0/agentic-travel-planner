from pydantic import BaseModel, Field, HttpUrl, model_validator
from datetime import date
from typing import Literal


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
        description="Activity budget",
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

    departure_city: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    travelers: int = Field(default=1, ge=1, le=20)
    travel_style: Literal["budget", "balanced", "comfort"] = "balanced"

    @model_validator(mode="after")
    def validate_travel_dates(self):
        if (self.start_date is None) != (self.end_date is None):
            raise ValueError("Provide both start_date and end_date.")

        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("end_date must not be before start_date.")

            if (self.end_date - self.start_date).days + 1 != self.duration_days:
                raise ValueError("Travel dates must match duration_days.")

        return self


class Activity(BaseModel):
    name: str
    description: str
    estimated_cost: float = Field(ge=0)
    source_url: HttpUrl | None = None


class TripCostBreakdown(BaseModel):
    transportation: float = Field(ge=0)
    accommodation: float = Field(ge=0)
    food: float = Field(ge=0)
    activities: float = Field(ge=0)
    local_transportation: float = Field(ge=0)

    @property
    def total(self) -> float:
        return round(
            self.transportation
            + self.accommodation
            + self.food
            + self.activities
            + self.local_transportation,
            2,
        )


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
        ge=0,
        description="Total estimated cost of all planned activities",
    )

    cost_breakdown: TripCostBreakdown | None = Field(
        default=None,
        description="Estimated full-trip costs across all categories",
    )

    budget_scope: Literal["activities", "full_trip"] = Field(
        default="activities",
        description="Indicates whether the estimate covers activities only or the full trip",
    )
