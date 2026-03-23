"use client";

import { useState, useEffect } from "react";
import { getFeed, type Story, type Moment } from "@/lib/api";
import StoryCard from "@/components/StoryCard";
import MomentCard from "@/components/MomentCard";
import Link from "next/link";

const CATEGORIES = [
  "all", "loss", "love", "identity", "work", "family",
  "fear", "joy", "change", "regret", "hope",
  "philosophy", "science", "craft", "culture", "wisdom",
];

function SkeletonCard() {
  return (
    <div className="flex items-center gap-4 md:gap-6 p-4 rounded-xl">
      <div className="w-6 skeleton h-4" />
      <div className="w-12 h-12 skeleton rounded-lg flex-shrink-0" />
      <div className="flex-1 space-y-2">
        <div className="skeleton h-4 w-3/4" />
        <div className="skeleton h-3 w-1/2" />
      </div>
      <div className="hidden md:block skeleton h-3 w-20" />
      <div className="skeleton h-3 w-10" />
    </div>
  );
}

function SkeletonFeatured() {
  return (
    <div className="glass-player rounded-xl p-6 md:p-8 border border-outline-variant/10 animate-pulse">
      <div className="flex flex-col md:flex-row gap-6 items-center">
        <div className="w-40 h-40 skeleton rounded-lg flex-shrink-0" />
        <div className="flex-1 space-y-4 w-full">
          <div className="skeleton h-8 w-3/4" />
          <div className="skeleton h-4 w-1/3" />
          <div className="flex gap-1 h-12 items-end">
            {[4, 8, 12, 10, 14, 6, 16, 10, 4].map((h, i) => (
              <div key={i} className="flex-1 skeleton rounded-full" style={{ height: `${h * 3}px` }} />
            ))}
          </div>
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 skeleton rounded-full" />
            <div className="skeleton h-3 w-24" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [stories, setStories] = useState<Story[]>([]);
  const [moments, setMoments] = useState<Moment[]>([]);
  const [category, setCategory] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getFeed(category === "all" ? undefined : category)
      .then((data) => {
        setStories(data.stories || []);
        setMoments(data.moments || []);
      })
      .catch(() => {
        setStories([]);
        setMoments([]);
      })
      .finally(() => setLoading(false));
  }, [category]);

  const featured = stories[0];
  const playlist = stories.slice(1);

  return (
    <div className="space-y-6 md:space-y-12">
      {/* Hero Section */}
      <div className="relative w-full rounded-xl overflow-hidden bg-surface-container-low min-h-[200px] md:min-h-[300px] flex items-center p-5 md:p-12 vinyl-glow animate-fade-in">
        <div className="relative z-10 max-w-lg space-y-4 md:space-y-6">
          <h2 className="text-2xl sm:text-4xl md:text-6xl font-extrabold tracking-tighter leading-tight">
            Press play on <br className="hidden sm:block" />someone&apos;s{" "}
            <span className="text-primary-container animate-text-glow">truth</span>.
          </h2>
          <p className="text-on-surface-variant/60 text-xs md:text-base max-w-sm animate-fade-in-up" style={{ animationDelay: "200ms" }}>
            Anonymous stories, produced as intimate audio experiences. Every voice matters. No name needed.
          </p>
          <Link
            href="/submit"
            className="inline-flex items-center gap-2 bg-primary-container text-on-primary px-6 py-3 md:px-8 md:py-4 rounded-full font-bold text-sm md:text-base hover:scale-105 active:scale-95 transition-all ripple-effect animate-fade-in-up"
            style={{ animationDelay: "400ms" }}
          >
            <span>Share Your Story</span>
            <span className="material-symbols-outlined text-lg md:text-2xl">arrow_forward</span>
          </Link>
        </div>

        {/* Rotating Vinyl Art — smaller on mobile */}
        <div className="absolute right-[-15%] top-[-15%] w-[220px] h-[220px] sm:w-[350px] sm:h-[350px] md:w-[500px] md:h-[500px] opacity-15 md:opacity-20">
          <div className="w-full h-full animate-spin-slow">
            <div className="w-full h-full rounded-full border-[16px] md:border-[30px] border-surface-container-lowest shadow-[inset_0_0_100px_rgba(249,115,22,0.2)] flex items-center justify-center">
              <div className="w-2/3 h-2/3 rounded-full border border-outline-variant/30 flex items-center justify-center">
                <div className="w-1/2 h-1/2 rounded-full bg-primary-container/20 border-4 md:border-8 border-surface-container-lowest" />
              </div>
            </div>
          </div>
        </div>

        {/* Floating sound waves decoration */}
        <div className="absolute bottom-3 md:bottom-4 left-1/2 -translate-x-1/2 flex items-end gap-1 opacity-20">
          {[3, 6, 10, 14, 10, 16, 8, 12, 6, 4, 8, 14, 10, 6].map((h, i) => (
            <div
              key={i}
              className="w-1 bg-primary-container rounded-full wave-bar active"
              style={{ height: `${h * 1.5}px`, animationDelay: `${i * 0.08}s` }}
            />
          ))}
        </div>
      </div>

      {/* Category Filter — horizontal scroll on mobile */}
      <div className="-mx-4 md:mx-0 px-4 md:px-0">
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-none animate-fade-in-up snap-x snap-mandatory" style={{ animationDelay: "300ms" }}>
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-4 md:px-5 py-2 rounded-full text-[10px] md:text-xs font-bold uppercase tracking-wide whitespace-nowrap transition-all duration-300 snap-start
                ${category === cat
                  ? "bg-primary-container text-on-primary scale-105 shadow-lg shadow-primary-container/20"
                  : "bg-surface-container text-on-surface-variant hover:bg-surface-container-high hover:scale-105"
                }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="space-y-8">
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
            <div className="xl:col-span-2 space-y-6">
              <div className="skeleton h-4 w-32 rounded-full" />
              <SkeletonFeatured />
            </div>
            <div className="space-y-4">
              <div className="skeleton h-4 w-28 rounded-full" />
              {[1, 2, 3].map((i) => (
                <div key={i} className="skeleton h-24 rounded-xl" />
              ))}
            </div>
          </div>
          <div className="space-y-6">
            <div className="skeleton h-8 w-48" />
            {[1, 2, 3, 4, 5].map((i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        </div>
      ) : (
        <>
          {/* Featured Story + B-Side Moments Grid */}
          {(featured || moments.length > 0) && (
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
              {/* Featured Story (Now Playing) */}
              {featured && (
                <div className="xl:col-span-2 space-y-6 animate-fade-in-up">
                  <h3 className="text-xs font-bold uppercase tracking-widest text-secondary flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
                    Featured Selection
                  </h3>
                  <Link href={`/story/${featured.id}`} className="block group">
                    <div className={`glass-player rounded-xl p-4 md:p-8 border border-outline-variant/10 shadow-2xl relative overflow-hidden card-hover emotion-${featured.emotion || "wonder"} emotion-glow`}>
                      <div className="flex flex-row md:flex-row gap-4 md:gap-6 items-center relative z-10">
                        {/* Album Art */}
                        <div className="relative w-20 h-20 md:w-40 md:h-40 flex-shrink-0">
                          <div className="absolute inset-0 bg-gradient-to-br from-primary-container to-secondary rounded-lg rotate-3 group-hover:rotate-6 transition-transform duration-500" />
                          <div className="relative w-full h-full bg-surface-container-highest rounded-lg shadow-lg flex items-center justify-center overflow-hidden">
                            <span className="material-symbols-outlined text-6xl text-primary/30 group-hover:scale-110 transition-transform duration-500">graphic_eq</span>
                            {/* Mini equalizer in album art */}
                            <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex items-end gap-[2px] opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                              {[1, 2, 3, 4, 5, 4, 3].map((_, i) => (
                                <div key={i} className={`eq-bar eq-bar-${(i % 4) + 1} bg-primary w-[2px]`} style={{ height: "12px" }} />
                              ))}
                            </div>
                          </div>
                        </div>
                        {/* Info */}
                        <div className="flex-1 space-y-2 md:space-y-3 w-full text-left">
                          <div>
                            <h4 className="text-lg md:text-3xl font-bold tracking-tight group-hover:text-primary transition-colors duration-300 line-clamp-2">
                              {featured.title}
                            </h4>
                            <p className="text-primary font-medium tracking-wide text-xs md:text-base">
                              {featured.category} &middot; {featured.audio_duration_secs ? `${Math.ceil(featured.audio_duration_secs / 60)} min` : ""}
                            </p>
                          </div>
                          {/* Waveform — hidden on small mobile */}
                          <div className="h-8 md:h-12 flex items-end gap-1 px-1 md:px-2">
                            {[4, 8, 12, 10, 14, 6, 16, 10, 4].map((h, i) => (
                              <div
                                key={i}
                                className="flex-1 bg-primary rounded-full wave-bar active"
                                style={{ height: `${h * 3}px`, animationDelay: `${i * 0.1}s`, opacity: 0.3 + i * 0.07 }}
                              />
                            ))}
                          </div>
                          {/* Snippet preview */}
                          {featured.anonymized_text && (
                            <p className="text-xs text-on-surface-variant/40 italic line-clamp-2 hidden md:block">
                              &ldquo;{featured.anonymized_text.slice(0, 150)}...&rdquo;
                            </p>
                          )}
                          {/* Play button */}
                          <div className="flex items-center gap-3 md:gap-4 pt-1 md:pt-2">
                            <div className="w-10 h-10 md:w-14 md:h-14 rounded-full bg-primary-container text-on-primary flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:shadow-primary-container/40 transition-all duration-300">
                              <span className="material-symbols-outlined text-xl md:text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
                                play_arrow
                              </span>
                            </div>
                            <span className="text-on-surface-variant/60 text-xs md:text-sm">
                              {featured.listen_count > 0 ? `${featured.listen_count.toLocaleString()} listens` : "Be the first"}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </div>
              )}

              {/* B-Side Moments */}
              {moments.length > 0 && (
                <div className="space-y-6 animate-fade-in-up" style={{ animationDelay: "150ms" }}>
                  <h3 className="text-xs font-bold uppercase tracking-widest text-secondary flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-secondary" />
                    B-Side Moments
                  </h3>
                  <div className="space-y-3 stagger-children">
                    {moments.slice(0, 4).map((m) => (
                      <MomentCard key={m.id} moment={m} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Story Feed (Playlist Style) */}
          {playlist.length > 0 && (
            <div className="space-y-6 animate-fade-in-up" style={{ animationDelay: "200ms" }}>
              <div className="flex items-end justify-between border-b border-outline-variant/10 pb-4">
                <div>
                  <h3 className="text-xl md:text-4xl font-extrabold tracking-tighter">Daily Playlist</h3>
                  <p className="text-on-surface-variant/60 font-medium">Curated stories from the archives</p>
                </div>
                <div className="hidden md:flex items-center gap-1 text-on-surface-variant/30">
                  <span className="material-symbols-outlined text-sm">queue_music</span>
                  <span className="text-xs font-bold">{playlist.length} stories</span>
                </div>
              </div>
              <div className="space-y-1 stagger-children">
                {playlist.map((story, i) => (
                  <StoryCard key={story.id} story={story} index={i + 1} />
                ))}
              </div>
            </div>
          )}

          {/* Empty state */}
          {stories.length === 0 && moments.length === 0 && (
            <div className="text-center py-16 animate-fade-in-up">
              <div className="w-20 h-20 rounded-full bg-surface-container-highest flex items-center justify-center mx-auto mb-6 animate-float">
                <span className="material-symbols-outlined text-4xl text-primary/40">mic</span>
              </div>
              <p className="text-on-surface-variant mb-2 text-lg font-medium">No stories yet</p>
              <p className="text-on-surface-variant/40 mb-6 text-sm">Be the first to share something real.</p>
              <Link
                href="/submit"
                className="inline-flex items-center gap-2 bg-primary-container text-on-primary px-6 py-3 rounded-full font-bold hover:scale-105 transition-transform ripple-effect"
              >
                Share Your Story
                <span className="material-symbols-outlined">arrow_forward</span>
              </Link>
            </div>
          )}
        </>
      )}
    </div>
  );
}
