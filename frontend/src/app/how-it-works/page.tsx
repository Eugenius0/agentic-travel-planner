import Link from "next/link";
import {
  ArrowRight,
  CheckCircle2,
  Compass,
  MapPinned,
  Sparkles,
  Wallet,
} from "lucide-react";
import Navbar from "@/components/Navbar";

const steps = [
  {
    number: "01",
    title: "Tell us about your trip",
    description:
      "Choose your destination, travel dates, number of travelers, interests, travel style, and total budget.",
    icon: Compass,
  },
  {
    number: "02",
    title: "AI researches your destination",
    description:
      "An AI research agent uses Tavily through MCP to find relevant destination information and useful sources.",
    icon: MapPinned,
  },
  {
    number: "03",
    title: "Your itinerary takes shape",
    description:
      "AI creates a personalized day-by-day travel plan and estimates transportation, accommodation, food, and activity costs.",
    icon: Sparkles,
  },
  {
    number: "04",
    title: "Your plan is validated",
    description:
      "The system checks itinerary structure and budget consistency, then attempts to correct plans that fail validation.",
    icon: CheckCircle2,
  },
];

export default function HowItWorksPage() {
  return (
    <main className="min-h-screen bg-[#f7fafc]">
      <Navbar />

      <section className="mx-auto max-w-5xl px-6 pb-24 pt-16 md:px-10">
        <div className="mx-auto max-w-2xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#dce8ef] bg-white px-4 py-2 text-sm font-medium text-[#477e9d]">
            <Sparkles size={16} />
            Your journey, simplified
          </div>

          <h1 className="text-4xl font-semibold tracking-tight text-[#253b4b] md:text-6xl">
            How it works
          </h1>

          <p className="mt-6 text-lg leading-relaxed text-[#718696]">
            From your first idea to a personalized travel itinerary, our
            AI-powered planner helps you explore more and plan smarter.
          </p>
        </div>

        <div className="mt-16 grid gap-6 md:grid-cols-2">
          {steps.map((step) => {
            const Icon = step.icon;

            return (
              <div
                key={step.number}
                className="rounded-[28px] border border-[#dce8ef] bg-white p-8 shadow-sm"
              >
                <div className="mb-7 flex items-center justify-between">
                  <div className="flex h-13 w-13 items-center justify-center rounded-2xl bg-[#eaf4fa] text-[#477e9d]">
                    <Icon size={25} />
                  </div>

                  <span className="text-sm font-semibold tracking-widest text-[#9ab4c4]">
                    {step.number}
                  </span>
                </div>

                <h2 className="text-xl font-semibold text-[#253b4b]">
                  {step.title}
                </h2>

                <p className="mt-3 leading-relaxed text-[#718696]">
                  {step.description}
                </p>
              </div>
            );
          })}
        </div>

        <div className="mt-10 rounded-[28px] border border-[#dce8ef] bg-[#eaf4fa] p-7 md:p-9">
          <div className="flex items-start gap-4">
            <Wallet size={25} className="mt-1 shrink-0 text-[#477e9d]" />

            <div>
              <h2 className="text-lg font-semibold text-[#253b4b]">
                Plan with your budget in mind
              </h2>

              <p className="mt-2 leading-relaxed text-[#718696]">
                Your estimated budget includes transportation, accommodation,
                food, activities, and local travel. Costs are estimates, not
                live booking quotes.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center">
          <Link
            href="/#plan"
            className="inline-flex items-center gap-3 rounded-full bg-[#477e9d] px-8 py-4 font-semibold text-white transition hover:bg-[#356783]"
          >
            Plan your trip
            <ArrowRight size={19} />
          </Link>
        </div>
      </section>
    </main>
  );
}
