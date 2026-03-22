"use client";

import { useState } from "react";
import { reactToStory, reactToMoment } from "@/lib/api";

const REACTIONS = [
  { type: "cry", icon: "water_drop", label: "Moved" },
  { type: "hug", icon: "volunteer_activism", label: "Comforted" },
  { type: "strong", icon: "fitness_center", label: "Inspired" },
  { type: "think", icon: "psychology", label: "Reflective" },
  { type: "heart", icon: "favorite", label: "Love" },
];

interface ReactionBarProps {
  targetId: string;
  targetType: "story" | "moment";
  initialCounts: Record<string, number>;
  meTooCount?: number;
}

export default function ReactionBar({ targetId, targetType, initialCounts, meTooCount }: ReactionBarProps) {
  const [counts, setCounts] = useState(initialCounts || {});
  const [reacted, setReacted] = useState<Set<string>>(new Set());
  const [justReacted, setJustReacted] = useState<string | null>(null);

  const getSessionId = () => {
    let id = typeof window !== "undefined" ? localStorage.getItem("voiceless_session") : null;
    if (!id) {
      id = crypto.randomUUID();
      if (typeof window !== "undefined") localStorage.setItem("voiceless_session", id);
    }
    return id;
  };

  const handleReact = async (reactionType: string) => {
    if (reacted.has(reactionType)) return;

    // Optimistic update with animation
    setJustReacted(reactionType);
    setCounts((prev) => ({ ...prev, [reactionType]: (prev[reactionType] || 0) + 1 }));
    setReacted((prev) => new Set(prev).add(reactionType));

    setTimeout(() => setJustReacted(null), 500);

    const sessionId = getSessionId();
    try {
      const fn = targetType === "story" ? reactToStory : reactToMoment;
      const result = await fn(targetId, reactionType, sessionId);
      if (result.reaction_counts) {
        setCounts(result.reaction_counts);
      }
    } catch {
      // Revert on failure
      setCounts((prev) => ({ ...prev, [reactionType]: Math.max(0, (prev[reactionType] || 0) - 1) }));
      setReacted((prev) => {
        const next = new Set(prev);
        next.delete(reactionType);
        return next;
      });
    }
  };

  const total = Object.values(counts).reduce((a, b) => a + b, 0);

  return (
    <div className="bg-surface-container-low rounded-xl p-5 border border-outline-variant/10 animate-fade-in-up">
      <div className="text-xs font-bold uppercase tracking-widest text-secondary mb-4">How did this make you feel?</div>
      <div className="flex gap-2 flex-wrap">
        {REACTIONS.map((r) => {
          const isReacted = reacted.has(r.type);
          const isJust = justReacted === r.type;
          return (
            <button
              key={r.type}
              onClick={() => handleReact(r.type)}
              disabled={isReacted}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-full border transition-all duration-300 text-sm font-medium
                ${isReacted
                  ? "border-primary-container/40 bg-primary-container/10 text-primary scale-105"
                  : "border-outline-variant/15 text-on-surface-variant/60 hover:border-primary-container/40 hover:text-primary hover:bg-primary-container/5 hover:scale-105 active:scale-95"
                }`}
            >
              <span
                className={`material-symbols-outlined text-lg transition-transform duration-300 ${isJust ? "animate-pop" : ""}`}
                style={isReacted ? { fontVariationSettings: "'FILL' 1" } : {}}
              >
                {r.icon}
              </span>
              <span className="tabular-nums">{counts[r.type] || 0}</span>
            </button>
          );
        })}
      </div>
      {total > 0 && (
        <div className="mt-4 text-sm text-on-surface-variant/50 flex items-center gap-2">
          <span className="material-symbols-outlined text-sm">group</span>
          {(meTooCount || total).toLocaleString()} people felt this too.
        </div>
      )}
    </div>
  );
}
