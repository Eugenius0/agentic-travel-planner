export type TravelRequest = {
  departure_city: string;
  destination: string;
  start_date: string;
  end_date: string;
  duration_days: number;
  travelers: number;
  budget: number;
  currency: string;
  interests: string[];
  travel_style: "budget" | "balanced" | "comfort";
};

export type Activity = {
  name: string;
  description: string;
  estimated_cost: number;
  source_url: string | null;
  category?: "activity" | "food";
};

export type DayPlan = {
  day: number;
  activities: Activity[];
};

export type TripCostBreakdown = {
  transportation: number;
  accommodation: number;
  food: number;
  activities: number;
  local_transportation: number;
};

export type TravelItinerary = {
  destination: string;
  currency: string;
  days: DayPlan[];
  total_estimated_cost: number;
  cost_breakdown: TripCostBreakdown | null;
  budget_scope: "activities" | "full_trip";
};

export async function generateTrip(
  request: TravelRequest,
): Promise<TravelItinerary> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/trips/plan`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to generate trip (HTTP ${response.status})`);
  }

  return response.json();
}
