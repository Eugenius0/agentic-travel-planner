import Navbar from "@/components/Navbar";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7fafc]">
      <Navbar />

      <section className="mx-auto max-w-7xl px-6 py-24 md:px-10">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-[#477e9d]">
          Your AI travel companion
        </p>

        <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-[#253b4b] md:text-7xl">
          Explore more.
          <br />
          Plan smarter.
        </h1>

        <p className="mt-6 max-w-xl text-lg leading-relaxed text-[#718696]">
          Discover extraordinary destinations, create personalized itineraries,
          and plan your entire trip around your budget.
        </p>
      </section>
    </main>
  );
}
