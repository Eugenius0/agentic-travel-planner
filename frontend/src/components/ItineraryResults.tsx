"use client";

import {
  ArrowUpRight,
  CalendarDays,
  CheckCircle2,
  Compass,
  MapPin,
  Wallet,
} from "lucide-react";

import type { TravelItinerary } from "@/lib/api";

type ItineraryResultsProps = {
  itinerary: TravelItinerary;
};

export default function ItineraryResults({ itinerary }: ItineraryResultsProps) {
  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: itinerary.currency,
      maximumFractionDigits: 2,
    }).format(amount);

  return (
    <section
      aria-label="Generated travel itinerary"
      className="mt-8 overflow-hidden rounded-[32px] border border-[#dce8ef] bg-white shadow-sm"
    >
      <div className="bg-[#d5eaf5] px-6 py-8 md:px-10 md:py-10">
        <div className="mb-5 flex items-center gap-2 text-sm font-semibold text-[#356783]">
          <CheckCircle2 size={18} />
          Your trip is ready
        </div>

        <h3 className="text-3xl font-semibold tracking-tight text-[#253b4b] md:text-4xl">
          Your journey to {itinerary.destination}
        </h3>

        <p className="mt-3 max-w-2xl text-[#58788b]">
          Explore your personalized day-by-day itinerary, discover activities,
          and review estimated costs.
        </p>

        <div className="mt-7 flex flex-wrap gap-3">
          <div className="flex items-center gap-2 rounded-full bg-white/80 px-4 py-2 text-sm font-medium text-[#253b4b]">
            <CalendarDays size={16} />
            {itinerary.days.length} days
          </div>

          <div className="flex items-center gap-2 rounded-full bg-white/80 px-4 py-2 text-sm font-medium text-[#253b4b]">
            <Wallet size={16} />
            {formatCurrency(itinerary.total_estimated_cost)} in activities
          </div>
        </div>
      </div>

      <div className="space-y-8 p-6 md:p-10">
        {itinerary.days.map((day) => {
          const dayTotal = day.activities.reduce(
            (sum, activity) => sum + activity.estimated_cost,
            0,
          );

          return (
            <article key={day.day}>
              <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#477e9d] text-sm font-semibold text-white">
                    {day.day}
                  </div>

                  <div>
                    <h4 className="text-xl font-semibold text-[#253b4b]">
                      Day {day.day}
                    </h4>

                    <p className="text-sm text-[#718696]">
                      {day.activities.length} planned activities
                    </p>
                  </div>
                </div>

                <span className="rounded-full bg-[#eaf4fa] px-4 py-2 text-sm font-medium text-[#356783]">
                  {formatCurrency(dayTotal)}
                </span>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                {day.activities.map((activity, index) => (
                  <div
                    key={`${day.day}-${index}`}
                    className="rounded-3xl border border-[#dce8ef] bg-[#f7fafc] p-5 transition hover:border-[#b9d6e6] hover:shadow-sm"
                  >
                    <div className="mb-4 flex items-center justify-between">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#eaf4fa] text-[#477e9d]">
                        <Compass size={19} />
                      </div>

                      <span className="text-sm font-semibold text-[#356783]">
                        {formatCurrency(activity.estimated_cost)}
                      </span>
                    </div>

                    <h5 className="text-lg font-semibold text-[#253b4b]">
                      {activity.name}
                    </h5>

                    <p className="mt-2 text-sm leading-6 text-[#718696]">
                      {activity.description}
                    </p>

                    {activity.source_url && (
                      <a
                        href={activity.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-[#477e9d] transition hover:text-[#356783]"
                      >
                        View source
                        <ArrowUpRight size={16} />
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </article>
          );
        })}

        <div className="rounded-3xl border border-[#dce8ef] bg-[#eaf4fa] p-6">
          <div className="flex items-center gap-2 text-[#356783]">
            <MapPin size={18} />
            <h4 className="text-lg font-semibold">Budget overview</h4>
          </div>

          <div className="mt-5 flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-sm text-[#718696]">
                Estimated activities total
              </p>

              <p className="mt-1 text-3xl font-semibold text-[#253b4b]">
                {formatCurrency(itinerary.total_estimated_cost)}
              </p>
            </div>

            <span className="rounded-full bg-white px-4 py-2 text-xs font-medium text-[#718696]">
              Activity costs only
            </span>
          </div>

          <p className="mt-4 text-sm leading-6 text-[#718696]">
            Accommodation, transportation, meals, and local transport are not
            included in this estimate yet.
          </p>
        </div>
      </div>
    </section>
  );
}
