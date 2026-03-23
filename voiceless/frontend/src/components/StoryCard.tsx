"use client";

import { useState } from "react";
import Link from "next/link";
import type { Story } from "@/lib/api";

const CATEGORY_ICONS: Record<string, string> = {
  loss: "water_drop",
  love: "favorite",
  identity: "person",
  work: "work",
  family: "group",
  fear: "bolt",
  joy: "celebration",
  change: "autorenew",
  regret: "history",
  hope: "light_mode",
  philosophy: "psychology",
  science: "science",
  craft: "brush",
  culture: "public",
  wisdom: "auto_awesome",
};

export default function StoryCard({ story, index }: { story: Story; index?: number }) {
  const [hovered, setHovered] = useState(false);
  const totalReactions = Object.values(story.reaction_counts || {}).reduce((a, b) => a + b, 0);
  const icon = CATEGORY_ICONS[story.category] || "graphic_eq";
  const emotionClass = `emotion-${story.emotion || "wonder"}`;

  const formatDuration = (secs?: number) => {
    if (!secs) return "";
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <Link href={`/story/${story.id}`} className="block group">
      <div
        className={`animate-fade-in-up ${emotionClass} emotion-glow card-hover flex items-center gap-3 md:gap-6 p-3 md:p-4 rounded-xl border border-transparent hover:bg-surface-container-high/60 transition-all cursor-pointer`}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {/* Track number */}
        {index !== undefined && (
          <div className="text-on-surface-variant/40 font-bold text-sm w-6 text-right tabular-nums group-hover:text-primary/60 transition-colors">
            {String(index).padStart(2, "0")}
          </div>
        )}

        {/* Category icon with equalizer on hover */}
        <div className="w-10 h-10 md:w-12 md:h-12 bg-surface-container-highest rounded-lg flex items-center justify-center relative flex-shrink-0 overflow-hidden">
          {/* Default icon */}
          <span className={`material-symbols-outlined text-primary/60 transition-all duration-300 ${hovered ? "opacity-0 scale-75" : "opacity-100 scale-100"}`}>
            {icon}
          </span>

          {/* Equalizer bars on hover */}
          <div className={`absolute inset-0 flex items-end justify-center gap-[3px] pb-2 transition-all duration-300 ${hovered ? "opacity-100" : "opacity-0"}`}>
            <div className="eq-bar eq-bar-1 bg-primary" style={{ height: "40%" }} />
            <div className="eq-bar eq-bar-2 bg-primary" style={{ height: "60%" }} />
            <div className="eq-bar eq-bar-3 bg-primary" style={{ height: "30%" }} />
            <div className="eq-bar eq-bar-4 bg-primary" style={{ height: "50%" }} />
          </div>
        </div>

        {/* Title + meta + snippet preview */}
        <div className="flex-1 min-w-0">
          <h6 className="font-bold text-sm md:text-base text-on-surface group-hover:text-primary transition-colors truncate">
            {story.title}
          </h6>
          <p className="text-[10px] md:text-xs text-on-surface-variant truncate">
            {story.category} &middot;{" "}
            {story.source_type === "cc_blog" ? "From the Archives" : "Anonymous Submission"}
          </p>
          {/* Story snippet — revealed on hover */}
          <div className={`overflow-hidden transition-all duration-400 ease-out ${hovered ? "max-h-12 opacity-100 mt-1.5" : "max-h-0 opacity-0 mt-0"}`}>
            <p className="text-xs text-on-surface-variant/50 italic line-clamp-2 leading-relaxed">
              &ldquo;{story.anonymized_text?.slice(0, 120)}{story.anonymized_text && story.anonymized_text.length > 120 ? "..." : ""}&rdquo;
            </p>
          </div>
        </div>

        {/* Listen count */}
        {story.listen_count > 0 && (
          <div className="hidden md:flex items-center gap-1.5 text-xs text-on-surface-variant/60 font-medium w-28">
            <span className="material-symbols-outlined text-sm">headphones</span>
            {story.listen_count.toLocaleString()}
          </div>
        )}

        {/* Duration */}
        <div className="hidden md:block text-xs text-on-surface-variant/60 font-medium tabular-nums w-14">
          {formatDuration(story.audio_duration_secs)}
        </div>

        {/* Play icon */}
        <div className="flex items-center gap-3 text-on-surface-variant">
          {totalReactions > 0 && (
            <span className="text-xs hidden md:inline text-on-surface-variant/40">{totalReactions}</span>
          )}
          <span
            className={`material-symbols-outlined text-xl transition-all duration-300 ${hovered ? "text-primary scale-110" : "text-on-surface-variant/40"}`}
            style={hovered ? { fontVariationSettings: "'FILL' 1" } : {}}
          >
            play_circle
          </span>
        </div>
      </div>
    </Link>
  );
}
