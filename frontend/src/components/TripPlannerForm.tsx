"use client";

import { useState, type FormEvent } from "react";
import {
  ArrowUpRight,
  CalendarDays,
  MapPin,
  Sparkles,
  Users,
  Wallet,
} from "lucide-react";

export default function TripPlannerForm() {
  const [departureCity, setDepartureCity] = useState("");
  const [destination, setDestination] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [travelers, setTravelers] = useState(1);
  const [budget, setBudget] = useState("");
  const [interests, setInterests] = useState<string[]>([]);
  const [travelStyle, setTravelStyle] = useState("balanced");

  const interestOptions = [
    "Nature",
    "Food",
    "Culture",
    "Museums",
    "Adventure",
    "Relaxation",
  ];

  function toggleInterest(interest: string) {
    setInterests((current) =>
      current.includes(interest)
        ? current.filter((item) => item !== interest)
        : [...current, interest],
    );
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (interests.length === 0) {
      alert("Please select at least one interest.");
      return;
    }

    console.log({
      departure_city: departureCity,
      destination,
      start_date: startDate,
      end_date: endDate,
      travelers,
      budget: Number(budget),
      currency: "EUR",
      interests,
      travel_style: travelStyle,
    });
  }

  const inputClass =
    "w-full rounded-2xl border border-[#dce8ef] bg-white px-4 py-3.5 text-[#253b4b] outline-none transition focus:border-[#477e9d] focus:ring-2 focus:ring-[#477e9d]/10";

  return (
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
            <MapPin size={16} /> Traveling from
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
            <MapPin size={16} /> Destination
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
            <CalendarDays size={16} /> Start date
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
            <CalendarDays size={16} /> End date
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
            <Users size={16} /> Travelers
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
            <Wallet size={16} /> Total budget (€)
          </span>
          <input
            required
            type="number"
            min={1}
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
          onChange={(event) => setTravelStyle(event.target.value)}
          className={inputClass}
        >
          <option value="budget">Budget-friendly</option>
          <option value="balanced">Balanced</option>
          <option value="comfort">Comfort</option>
        </select>
      </div>

      <button
        type="submit"
        className="mt-9 flex w-full items-center justify-center gap-3 rounded-full bg-[#477e9d] px-7 py-4 font-semibold text-white transition hover:bg-[#356783]"
      >
        Generate my trip
        <ArrowUpRight size={19} />
      </button>
    </form>
  );
}
