import Image from "next/image";
import { Sparkles } from "lucide-react";
import Navbar from "@/components/Navbar";
import DestinationCard from "@/components/DestinationCard";
import TripPlannerForm from "@/components/TripPlannerForm";

const destinations = [
  {
    name: "Amalfi Coast",
    country: "Italy",
    image: "/images/amalfi.jpg",
    description: "Coastal villages and Mediterranean charm.",
  },
  {
    name: "Kyoto",
    country: "Japan",
    image: "/images/kyoto.jpg",
    description: "Ancient temples and timeless traditions.",
  },
  {
    name: "Lofoten Islands",
    country: "Norway",
    image: "/images/lofoten.jpg",
    description: "Dramatic mountains and Arctic landscapes.",
  },
  {
    name: "Marrakech",
    country: "Morocco",
    image: "/images/marrakech.jpg",
    description: "Colorful markets and historic architecture.",
  },
  {
    name: "Bali",
    country: "Indonesia",
    image: "/images/bali.jpg",
    description: "Tropical landscapes and peaceful retreats.",
  },
  {
    name: "New York",
    country: "United States",
    image: "/images/ny.jpg",
    description: "Iconic streets and vibrant city life.",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7fafc]">
      <Navbar />

      {/* Main trip planning section */}
      <section
        id="plan"
        className="relative isolate scroll-mt-8 overflow-hidden px-6 py-4 md:px-10 md:py-[clamp(8px,2dvh,32px)]"
      >
        {/* Scenic background */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <Image
            src="/images/destination.jpg"
            alt=""
            fill
            priority
            sizes="100vw"
            className="scale-105 object-cover blur-[3px]"
          />
          <div className="absolute inset-0 bg-[#edf5fa]/45" />
        </div>

        <div className="mx-auto max-w-4xl">
          <div className="mb-[clamp(8px,1.5dvh,20px)] text-center">
            <div className="mb-[clamp(4px,1dvh,12px)] inline-flex items-center gap-2 rounded-full border border-white/70 bg-white/85 px-4 py-2 text-sm font-medium text-[#477e9d] shadow-sm">
              <Sparkles size={16} />
              Your AI travel companion
            </div>

            <h1 className="text-3xl font-semibold tracking-tight text-[#253b4b] md:text-4xl">
              Explore more. Plan smarter.
            </h1>

            <p className="mx-auto mt-2 max-w-xl text-base leading-relaxed text-[#253b4b] md:text-lg">
              Create a personalized travel itinerary around your interests,
              dates, and budget.
            </p>
          </div>

          <TripPlannerForm />
        </div>
      </section>

      {/* Discover section */}
      <section
        id="explore"
        className="mx-auto w-full max-w-7xl scroll-mt-8 px-6 py-16 md:px-10 md:py-20"
      >
        <div className="mb-8">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#477e9d]">
            Discover
          </p>

          <h2 className="text-3xl font-semibold tracking-tight text-[#253b4b] md:text-4xl">
            Somewhere worth exploring.
          </h2>

          <p className="mt-3 text-[#718696]">
            Find inspiration for your next adventure, then plan it your way.
          </p>
        </div>

        <div className="grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {destinations.map((destination) => (
            <DestinationCard key={destination.name} {...destination} />
          ))}
        </div>
      </section>
    </main>
  );
}
