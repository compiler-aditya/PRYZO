"use client";

import { useState, useEffect, use } from "react";
import { getStory, type Story } from "@/lib/api";
import AudioPlayer from "@/components/AudioPlayer";
import ReactionBar from "@/components/ReactionBar";
import TimeCapsule from "@/components/TimeCapsule";
import YoureNotAlone from "@/components/YoureNotAlone";
import ReflectionWidget from "@/components/ReflectionWidget";
import IdentityPromise from "@/components/IdentityPromise";
import Link from "next/link";

export default function StoryPage({ params }: { params: { id: string } | Promise<{ id: string }> }) {
  const { id } = params instanceof Promise ? use(params) : params;
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStory(id)
      .then(setStory)
      .catch(() => setStory(null))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <div className="skeleton w-6 h-6 rounded-full" />
          <div className="skeleton h-6 w-24 rounded-full" />
        </div>
        <div className="glass-player rounded-xl p-6 md:p-8 border border-outline-variant/10">
          <div className="flex flex-col md:flex-row gap-6 items-center">
            <div className="w-40 h-40 skeleton rounded-lg flex-shrink-0" />
            <div className="flex-1 space-y-4 w-full">
              <div className="skeleton h-8 w-3/4" />
              <div className="flex gap-[2px] h-16 items-end">
                {Array.from({ length: 40 }).map((_, i) => (
                  <div key={i} className="flex-1 skeleton rounded-full" style={{ height: `${20 + (i * 7 % 60)}%` }} />
                ))}
              </div>
              <div className="skeleton h-2 w-full rounded-full" />
              <div className="flex items-center gap-6">
                <div className="skeleton w-14 h-14 rounded-full" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!story) {
    return (
      <div className="text-center py-16 animate-fade-in">
        <div className="w-16 h-16 rounded-full bg-surface-container-highest flex items-center justify-center mx-auto mb-4">
          <span className="material-symbols-outlined text-3xl text-on-surface-variant/40">search_off</span>
        </div>
        <p className="text-on-surface-variant mb-4">Story not found.</p>
        <Link href="/" className="text-primary hover:underline text-sm">Back to stories</Link>
      </div>
    );
  }

  const sourceLabel =
    story.source_type === "cc_blog"
      ? `From the Archives ${story.time_capsule?.era ? `\u00B7 ${story.time_capsule.era}` : ""}`
      : "Anonymous Submission";

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Back + Category badge */}
      <div className="flex items-center gap-4 animate-fade-in">
        <Link href="/" className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">
          arrow_back
        </Link>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-primary-container/10 text-primary text-xs font-bold uppercase tracking-wide rounded-full">
            {story.category}
          </span>
          {story.emotion && (
            <span className={`px-3 py-1 text-xs font-bold uppercase tracking-wide rounded-full bg-surface-container text-on-surface-variant/60`}>
              {story.emotion}
            </span>
          )}
          <span className="text-xs text-on-surface-variant/40">{sourceLabel}</span>
        </div>
      </div>

      {/* Audio player */}
      {story.audio_url ? (
        <AudioPlayer
          audioUrl={story.audio_url}
          title={story.title}
          storyId={story.id}
          duration={story.audio_duration_secs}
          text={story.anonymized_text}
          emotion={story.emotion}
        />
      ) : (
        <div className="glass-player rounded-xl p-6 md:p-8 border border-outline-variant/10 shadow-2xl animate-fade-in-up">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-4">
            {story.title}
          </h2>
          <p className="text-on-surface-variant leading-relaxed italic">
            &ldquo;{story.anonymized_text}&rdquo;
          </p>
          {story.status === "producing" && (
            <div className="mt-4 flex items-center gap-2 text-secondary text-sm">
              <div className="flex items-end gap-[2px]">
                <div className="eq-bar eq-bar-1 bg-secondary w-[2px]" style={{ height: "10px" }} />
                <div className="eq-bar eq-bar-2 bg-secondary w-[2px]" style={{ height: "10px" }} />
                <div className="eq-bar eq-bar-3 bg-secondary w-[2px]" style={{ height: "10px" }} />
              </div>
              Audio is being produced...
            </div>
          )}
        </div>
      )}

      {/* Identity promise */}
      <div className="animate-fade-in-up" style={{ animationDelay: "100ms" }}>
        <IdentityPromise compact />
      </div>

      {/* Time Capsule */}
      {story.time_capsule && (
        <div className="animate-fade-in-up" style={{ animationDelay: "200ms" }}>
          <TimeCapsule
            era={story.time_capsule.era}
            facts={story.time_capsule.facts}
            cultural_context={story.time_capsule.cultural_context}
            statistics={story.time_capsule.statistics}
          />
        </div>
      )}

      {/* Reactions */}
      <div className="animate-fade-in-up" style={{ animationDelay: "300ms" }}>
        <ReactionBar
          targetId={story.id}
          targetType="story"
          initialCounts={story.reaction_counts}
          meTooCount={story.me_too_count}
        />
      </div>

      {/* You're Not Alone */}
      {story.similar_stories && story.similar_stories.length > 0 && (
        <div className="animate-fade-in-up" style={{ animationDelay: "400ms" }}>
          <YoureNotAlone stories={story.similar_stories} />
        </div>
      )}

      {/* Reflection companion */}
      <div className="animate-fade-in-up" style={{ animationDelay: "500ms" }}>
        <ReflectionWidget
          storyTheme={story.category}
          emotion={story.emotion}
          era={story.time_capsule?.era}
        />
      </div>

      {/* Share prompt */}
      <div className="text-center py-4 animate-fade-in-up" style={{ animationDelay: "600ms" }}>
        <Link
          href={`/submit?category=${story.category}`}
          className="inline-flex items-center gap-2 bg-surface-container border border-outline-variant/10 text-on-surface-variant px-6 py-3 rounded-full text-sm font-medium hover:border-primary-container/30 hover:text-primary hover:scale-105 transition-all ripple-effect"
        >
          <span className="material-symbols-outlined text-lg">edit</span>
          Share YOUR story about {story.category}
        </Link>
      </div>
    </div>
  );
}
