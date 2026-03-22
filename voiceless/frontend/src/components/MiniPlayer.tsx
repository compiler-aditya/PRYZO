"use client";

import { useEffect, useState, useRef } from "react";
import Link from "next/link";

/**
 * MiniPlayer — persistent floating audio bar.
 * Owns the SINGLE shared audio element used by both MiniPlayer and AudioPlayer.
 * Exposes it as window.__voicelessAudio so AudioPlayer can control the same element.
 */

interface NowPlaying {
  audioUrl: string;
  title: string;
  storyId: string;
  emotion?: string;
}

declare global {
  interface Window {
    __voicelessAudio?: HTMLAudioElement;
  }
}

export default function MiniPlayer() {
  const [nowPlaying, setNowPlaying] = useState<NowPlaying | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Create the ONE shared audio element for the entire app
    const audio = new Audio();
    audioRef.current = audio;
    window.__voicelessAudio = audio;

    audio.addEventListener("timeupdate", () => {
      setCurrentTime(audio.currentTime);
      if (audio.duration) setProgress((audio.currentTime / audio.duration) * 100);
    });
    audio.addEventListener("loadedmetadata", () => setDuration(audio.duration));
    audio.addEventListener("ended", () => setIsPlaying(false));
    audio.addEventListener("play", () => setIsPlaying(true));
    audio.addEventListener("pause", () => setIsPlaying(false));

    // "voiceless:track" — update displayed track info (AudioPlayer sends this)
    const handleTrackEvent = (e: Event) => {
      const detail = (e as CustomEvent<NowPlaying>).detail;
      setNowPlaying(detail);
    };

    window.addEventListener("voiceless:track", handleTrackEvent);

    return () => {
      window.removeEventListener("voiceless:track", handleTrackEvent);
      delete window.__voicelessAudio;
      audio.pause();
      audio.src = "";
    };
  }, []);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio || !nowPlaying) return;
    if (isPlaying) audio.pause();
    else audio.play().catch(() => {});
  };

  const seek = (e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current;
    if (!audio || !duration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const fraction = (e.clientX - rect.left) / rect.width;
    audio.currentTime = fraction * duration;
  };

  const close = () => {
    const audio = audioRef.current;
    if (audio) {
      audio.pause();
      audio.src = "";
    }
    setNowPlaying(null);
    setProgress(0);
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  if (!nowPlaying) return null;

  return (
    <div className="fixed bottom-10 left-0 right-0 z-[45] px-4 md:px-6 animate-fade-in-up">
      <div className="max-w-[1200px] mx-auto">
        <div className={`bg-surface-container-highest/95 backdrop-blur-xl rounded-2xl border border-outline-variant/15 shadow-2xl overflow-hidden emotion-${nowPlaying.emotion || "wonder"}`}>
          {/* Progress bar — clickable thin line at top */}
          <div className="h-1 bg-surface-container cursor-pointer" onClick={seek}>
            <div
              className="h-full bg-primary transition-all duration-200"
              style={{ width: `${progress}%` }}
            />
          </div>

          <div className="flex items-center gap-3 px-4 py-3">
            {/* Equalizer / album art mini */}
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center flex-shrink-0 overflow-hidden">
              {isPlaying ? (
                <div className="flex items-end gap-[2px] h-5">
                  <div className="eq-bar eq-bar-1 bg-primary w-[2px]" style={{ height: "8px" }} />
                  <div className="eq-bar eq-bar-2 bg-primary w-[2px]" style={{ height: "8px" }} />
                  <div className="eq-bar eq-bar-3 bg-primary w-[2px]" style={{ height: "8px" }} />
                  <div className="eq-bar eq-bar-4 bg-primary w-[2px]" style={{ height: "8px" }} />
                </div>
              ) : (
                <span className="material-symbols-outlined text-primary/50 text-lg">graphic_eq</span>
              )}
            </div>

            {/* Title */}
            <Link href={`/story/${nowPlaying.storyId}`} className="flex-1 min-w-0">
              <p className="text-sm font-bold text-on-surface truncate hover:text-primary transition-colors">
                {nowPlaying.title}
              </p>
              <p className="text-[10px] text-on-surface-variant/40 tabular-nums">
                {formatTime(currentTime)} / {formatTime(duration)}
              </p>
            </Link>

            {/* Play/Pause */}
            <button
              onClick={togglePlay}
              className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-300 ${
                isPlaying
                  ? "bg-primary-container text-on-primary play-btn-active"
                  : "bg-surface-container text-on-surface-variant hover:bg-primary-container hover:text-on-primary"
              }`}
            >
              <span
                className="material-symbols-outlined text-xl"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                {isPlaying ? "pause" : "play_arrow"}
              </span>
            </button>

            {/* Close */}
            <button
              onClick={close}
              className="text-on-surface-variant/30 hover:text-on-surface-variant transition-colors flex-shrink-0"
            >
              <span className="material-symbols-outlined text-lg">close</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
