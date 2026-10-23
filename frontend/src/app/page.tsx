import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, MapPin, Sparkles } from "lucide-react";
import Navbar from "@/components/Navbar";
import DestinationCard from "@/components/DestinationCard";

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
    <>
      <section id="explore" className="mx-auto max-w-7xl px-6 py-20 md:px-10">
        <div className="mb-8">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-[#477e9d]">
            Discover
          </p>

          <h2 className="text-3xl font-semibold tracking-tight text-[#253b4b] md:text-4xl">
            Somewhere worth exploring.
          </h2>

          <p className="mt-3 text-[#718696]">
            Beautiful destinations, thoughtfully planned around you.
          </p>
        </div>

        <div className="max-w-sm">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {destinations.map((destination) => (
              <DestinationCard key={destination.name} {...destination} />
            ))}
          </div>
        </div>
      </section>
      <main className="min-h-screen bg-[#f7fafc]">
        <Navbar />

        <section className="mx-auto grid max-w-7xl items-center gap-12 px-6 py-12 md:px-10 lg:grid-cols-2 lg:gap-16 lg:py-20">
          <div>
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-[#dce8ef] bg-white px-4 py-2 text-sm font-medium text-[#477e9d]">
              <Sparkles size={16} />
              Your AI travel companion
            </div>

            <h1 className="text-5xl leading-[1.08] font-semibold tracking-tight text-[#253b4b] md:text-6xl xl:text-7xl">
              Explore more.
              <br />
              Plan smarter.
            </h1>

            <p className="mt-7 max-w-lg text-lg leading-relaxed text-[#718696]">
              Discover extraordinary destinations, create personalized
              itineraries, and plan your entire trip around your budget.
            </p>

            <div className="mt-9 flex flex-wrap items-center gap-4">
              <Link
                href="/#plan"
                className="inline-flex items-center gap-3 rounded-full bg-[#477e9d] px-7 py-4 font-medium text-white transition-colors hover:bg-[#356783]"
              >
                Start planning
                <ArrowUpRight size={19} />
              </Link>

              <Link
                href="/#how-it-works"
                className="px-4 py-3 font-medium text-[#477e9d] hover:text-[#253b4b]"
              >
                How it works
              </Link>
            </div>
          </div>

          <div className="relative">
            <div className="relative h-[440px] overflow-hidden rounded-[32px] bg-[#d5eaf5] shadow-xl shadow-[#477e9d]/10 md:h-[540px]">
              <Image
                src="/images/destination.jpg"
                alt="Scenic travel destination"
                fill
                priority
                sizes="(max-width: 1024px) 100vw, 50vw"
                className="object-cover"
              />

              <div className="absolute inset-0 bg-gradient-to-t from-black/35 via-transparent to-transparent" />

              <div className="absolute right-6 bottom-6 left-6 flex items-center gap-2 text-white">
                <MapPin size={18} />
                <span className="text-sm font-medium">
                  Your next adventure awaits
                </span>
              </div>
            </div>

            <div className="absolute -bottom-5 -left-5 rounded-2xl border border-white/70 bg-white/90 px-5 py-4 shadow-lg backdrop-blur-md">
              <div className="flex items-center gap-2 text-sm font-semibold text-[#253b4b]">
                <Sparkles size={17} className="text-[#477e9d]" />
                Thoughtfully planned by AI
              </div>
              <p className="mt-1 text-xs text-[#718696]">
                Personalized to your budget and interests
              </p>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}
