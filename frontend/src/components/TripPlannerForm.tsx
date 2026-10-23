"use client";

import { useEffect, useState, type SubmitEvent } from "react";
import {
  ArrowUpRight,
  CalendarDays,
  MapPin,
  Sparkles,
  Users,
  Wallet,
} from "lucide-react";

import { generateTrip, type TravelItinerary } from "@/lib/api";
import ItineraryResults from "@/components/ItineraryResults";

const interestOptions = [
  "Nature",
  "Food",
  "Culture",
  "Museums",
  "Adventure",
  "Relaxation",
];

const inputClass =
  "w-full rounded-2xl border border-[#dce8ef] bg-white px-4 py-3.5 text-[#253b4b] outline-none transition focus:border-[#477e9d] focus:ring-2 focus:ring-[#477e9d]/10";

export default function TripPlannerForm() {
  const [departureCity, setDepartureCity] = useState("");
  const [destination, setDestination] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const selectedDestination = params.get("destination");

    if (selectedDestination) {
      setDestination(selectedDestination);
    }
  }, []);

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [travelers, setTravelers] = useState(1);
  const [budget, setBudget] = useState("");
  const [interests, setInterests] = useState<string[]>([]);
  const [travelStyle, setTravelStyle] = useState<
    "budget" | "balanced" | "comfort"
  >("balanced");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [itinerary, setItinerary] = useState<TravelItinerary | null>(null);
  const [submittedBudget, setSubmittedBudget] = useState<number | null>(null);

  function toggleInterest(interest: string) {
    setInterests((current) =>
      current.includes(interest)
        ? current.filter((item) => item !== interest)
        : [...current, interest],
    );
  }

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    setError(null);
    setItinerary(null);
    setSubmittedBudget(null);

    if (interests.length === 0) {
      setError("Please select at least one interest.");
      return;
    }

    const start = new Date(`${startDate}T00:00:00Z`);
    const end = new Date(`${endDate}T00:00:00Z`);

    const durationDays =
      Math.round((end.getTime() - start.getTime()) / 86400000) + 1;

    if (
      !Number.isFinite(durationDays) ||
      durationDays < 1 ||
      durationDays > 30
    ) {
      setError("Please select a trip duration between 1 and 30 days.");
      return;
    }

    setIsLoading(true);

    try {
      const result = await generateTrip({
        departure_city: departureCity.trim(),
        destination: destination.trim(),
        start_date: startDate,
        end_date: endDate,
        duration_days: durationDays,
        travelers,
        budget: Number(budget),
        currency: "EUR",
        interests,
        travel_style: travelStyle,
      });

      setItinerary(result);
      setSubmittedBudget(Number(budget));
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while generating your trip.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="rounded-[32px] border border-[#dce8ef] bg-[#eaf4fa] p-6 shadow-sm md:p-10"
      >
        <div className="mb-8 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#477e9d] text-white">
            <Sparkles size={23} />
          </div>

          <div>
            <h3 className="text-2xl font-semibold tracking-tight text-[#253b4b]">
              Design your next adventure
            </h3>

            <p className="text-sm text-[#718696]">
              Tell us what matters. AI will handle the planning.
            </p>
          </div>
        </div>

        <div className="grid gap-5 md:grid-cols-2">
          <label className="block">
            <span className="mb-2 flex items-center gap-2 text-sm font-medium text-[#253b4b]">
              <MapPin size={16} />
              Traveling from
            </span>

            <input
              required
              value={departureCity}
              onChange={(event) => setDepartureCity(event.target.value)}
              placeholder="Stockholm, Sweden"
              className={inputClass}
            />
          </label>

          <label className="block">
            <span className="mb-2 flex items-center gap-2 text-sm font-medium text-[#253b4b]">
              <MapPin size={16} />
              Destination
            </span>

            <input
              required
              value={destination}
              onChange={(event) => setDestination(event.target.value)}
              placeholder="Rome, Italy"
              className={inputClass}
            />
          </label>

          <label className="block">
            <span className="mb-2 flex items-center gap-2 text-sm font-medium text-[#253b4b]">
              <CalendarDays size={16} />
              Start date
            </span>

            <input
              required
              type="date"
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
              className={inputClass}
            />
          </label>

          <label className="block">
            <span className="mb-2 flex items-center gap-2 text-sm font-medium text-[#253b4b]">
              <CalendarDays size={16} />
              End date
            </span>

            <input
              required
              type="date"
              min={startDate || undefined}
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
              className={inputClass}
            />
          </label>

          <label className="block">
            <span className="mb-2 flex items-center gap-2 text-sm font-medium text-[#253b4b]">
              <Users size={16} />
              Travelers
            </span>

            <input
              required
              type="number"
              min={1}
              max={20}
              value={travelers}
              onChange={(event) => setTravelers(Number(event.target.value))}
              className={inputClass}
            />
          </label>

          <label className="block">
            <span className="mb-2 flex items-center gap-2 text-sm font-medium text-[#253b4b]">
              <Wallet size={16} />
              Total budget (€)
            </span>

            <input
              required
              type="number"
              min={1}
              step="0.01"
              value={budget}
              onChange={(event) => setBudget(event.target.value)}
              placeholder="1500"
              className={inputClass}
            />
          </label>
        </div>

        <div className="mt-8">
          <p className="mb-3 text-sm font-medium text-[#253b4b]">
            What are you interested in?
          </p>

          <div className="flex flex-wrap gap-2">
            {interestOptions.map((interest) => {
              const selected = interests.includes(interest);

              return (
                <button
                  key={interest}
                  type="button"
                  aria-pressed={selected}
                  onClick={() => toggleInterest(interest)}
                  className={`rounded-full border px-4 py-2.5 text-sm font-medium transition ${
                    selected
                      ? "border-[#477e9d] bg-[#477e9d] text-white"
                      : "border-[#dce8ef] bg-white text-[#718696] hover:border-[#477e9d]"
                  }`}
                >
                  {interest}
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-8">
          <label
            htmlFor="travel-style"
            className="mb-2 block text-sm font-medium text-[#253b4b]"
          >
            Travel style
          </label>

          <select
            id="travel-style"
            value={travelStyle}
            onChange={(event) =>
              setTravelStyle(
                event.target.value as "budget" | "balanced" | "comfort",
              )
            }
            className={inputClass}
          >
            <option value="budget">Budget-friendly</option>
            <option value="balanced">Balanced</option>
            <option value="comfort">Comfort</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="mt-9 flex w-full items-center justify-center gap-3 rounded-full bg-[#477e9d] px-7 py-4 font-semibold text-white transition hover:bg-[#356783] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? (
            <>
              <span className="h-5 w-5 animate-spin rounded-full border-2 border-white/40 border-t-white" />
              Researching and planning your trip...
            </>
          ) : (
            <>
              Generate my trip
              <ArrowUpRight size={19} />
            </>
          )}
        </button>

        {error && (
          <p role="alert" className="mt-4 text-center text-sm text-red-600">
            {error}
          </p>
        )}
      </form>

      {itinerary && submittedBudget !== null && (
        <ItineraryResults itinerary={itinerary} budget={submittedBudget} />
      )}
    </>
  );
}
