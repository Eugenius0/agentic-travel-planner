import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, MapPin, Sparkles } from "lucide-react";
import Navbar from "@/components/Navbar";

export default function Home() {
  return (
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
  );
}
