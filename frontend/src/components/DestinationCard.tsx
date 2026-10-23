import Image from "next/image";
import { ArrowUpRight, MapPin } from "lucide-react";

type DestinationCardProps = {
  name: string;
  country: string;
  image: string;
  description?: string;
};

export default function DestinationCard({
  name,
  country,
  image,
  description,
}: DestinationCardProps) {
  return (
    <article className="group overflow-hidden rounded-[28px] border border-[#dce8ef] bg-white p-3 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-[#477e9d]/10">
      <div className="relative h-56 overflow-hidden rounded-[20px] bg-[#d5eaf5]">
        <Image
          src={image}
          alt={`${name}, ${country}`}
          fill
          sizes="(max-width: 768px) 100vw, 33vw"
          className="object-cover transition-transform duration-500 group-hover:scale-105"
        />
      </div>

      <div className="flex items-start justify-between gap-3 px-2 pb-2 pt-5">
        <div>
          <h3 className="text-xl font-semibold tracking-tight text-[#253b4b]">
            {name}
          </h3>

          <p className="mt-1 flex items-center gap-1.5 text-sm text-[#718696]">
            <MapPin size={14} />
            {country}
          </p>

          {description && (
            <p className="mt-3 text-sm leading-relaxed text-[#718696]">
              {description}
            </p>
          )}
        </div>

        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#eaf4fa] text-[#477e9d] transition-colors group-hover:bg-[#477e9d] group-hover:text-white">
          <ArrowUpRight size={19} />
        </div>
      </div>
    </article>
  );
}
