import Link from "next/link";
import { ArrowUpRight, Compass } from "lucide-react";

export default function Navbar() {
  return (
    <header className="w-full">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 md:px-10">
        <Link href="/" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#477e9d] text-white">
            <Compass size={23} strokeWidth={2} />
          </div>

          <span className="text-lg font-semibold tracking-tight text-[#253b4b]">
            Agentic Travel
          </span>
        </Link>

        <div className="hidden items-center gap-9 md:flex">
          <Link
            href="/#explore"
            className="text-sm font-medium text-[#718696] transition-colors hover:text-[#253b4b]"
          >
            Explore
          </Link>

          <Link
            href="/#how-it-works"
            className="text-sm font-medium text-[#718696] transition-colors hover:text-[#253b4b]"
          >
            How it works
          </Link>
        </div>

        <Link
          href="/#plan"
          className="flex items-center gap-2 rounded-full bg-[#477e9d] px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-[#356783]"
        >
          Plan a trip
          <ArrowUpRight size={16} />
        </Link>
      </nav>
    </header>
  );
}
