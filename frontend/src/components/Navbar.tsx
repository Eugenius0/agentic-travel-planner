import Link from "next/link";
import { Compass } from "lucide-react";

export default function Navbar() {
  return (
    <header className="w-full">
      <nav className="mx-auto grid max-w-7xl grid-cols-[1fr_auto] items-center gap-4 px-6 py-4 md:grid-cols-[1fr_auto_1fr] md:px-10">
        <Link href="/" className="flex items-center gap-3 justify-self-start">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-[#477e9d] text-white">
            <Compass size={23} strokeWidth={2} />
          </div>

          <span className="text-lg font-semibold tracking-tight text-[#253b4b]">
            Agentic Travel
          </span>
        </Link>

        <div className="flex items-center gap-5 md:gap-9">
          <Link
            href="/#explore"
            className="text-sm font-medium text-[#718696] transition-colors hover:text-[#253b4b]"
          >
            Explore
          </Link>

          <Link
            href="/how-it-works"
            className="text-sm font-medium text-[#718696] transition-colors hover:text-[#253b4b]"
          >
            How it works
          </Link>
        </div>

        <div className="hidden md:block" aria-hidden="true" />
      </nav>
    </header>
  );
}
