"use client";

import { useState, useRef, useEffect, useMemo } from "react";

interface AudioPlayerProps {
  audioUrl: string;
  title: string;
  storyId?: string;
  duration?: number;
  text?: string;
  emotion?: string;
}

// Generate deterministic waveform heights from title string
function generateWaveform(seed: string, count: number): number[] {
  const heights: number[] = [];
  for (let i = 0; i < count; i++) {
    const charCode = seed.charCodeAt(i % seed.length) || 50;
    heights.push(20 + ((charCode * (i + 1) * 7) % 60));
  }
  return heights;
}

export default function AudioPlayer({ audioUrl, title, storyId, duration, text, emotion }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [shared, setShared] = useState(false);
  const listenRecorded = useRef(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [totalDuration, setTotalDuration] = useState(duration || 0);
  const waveformBars = useMemo(() => generateWaveform(title, 40), [title]);
  const emotionClass = `emotion-${emotion || "wonder"}`;

  useEffect(() => {
    // Use the shared audio element from MiniPlayer (single source of truth)
    const audio = window.__voicelessAudio || new Audio();
    audioRef.current = audio;

    // Load track into shared audio
    const resolvedUrl = new URL(audioUrl, window.location.href).href;
    if (!audio.src || audio.src !== resolvedUrl) {
      audio.src = audioUrl;
      audio.load();
    }

    // Sync initial state (audio might already be playing from MiniPlayer)
    setIsPlaying(!audio.paused);
    if (audio.currentTime > 0) setCurrentTime(audio.currentTime);
    if (audio.duration) setTotalDuration(audio.duration);

    // Tell MiniPlayer about this track
    window.dispatchEvent(new CustomEvent("voiceless:track", {
      detail: { audioUrl, title, storyId, emotion },
    }));

    // Listen to native audio events — since both components share the same
    // audio element, state stays in sync automatically
    const onTimeUpdate = () => setCurrentTime(audio.currentTime);
    const onLoadedMetadata = () => setTotalDuration(audio.duration);
    const onEnded = () => setIsPlaying(false);
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);

    return () => {
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
      // Audio keeps playing in MiniPlayer when navigating away — no cleanup needed
    };
  }, [audioUrl, title, storyId, emotion]);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
      // Record listen once per session
      if (storyId && !listenRecorded.current) {
        listenRecorded.current = true;
        import("@/lib/api").then(({ recordListen }) => recordListen(storyId)).catch(() => {});
      }
    }
  };

  const seek = (e: React.MouseEvent<HTMLDivElement>) => {
    const audio = audioRef.current;
    if (!audio || !totalDuration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const fraction = (e.clientX - rect.left) / rect.width;
    audio.currentTime = fraction * totalDuration;
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  const progress = totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0;

  // For text reveal: calculate how much text to show
  const revealedLength = text ? Math.floor((progress / 100) * text.length) : 0;

  return (
    <div className={`glass-player rounded-xl p-6 md:p-8 border border-outline-variant/10 shadow-2xl relative overflow-hidden ${emotionClass} animate-fade-in-up`}>
      {/* No <audio> element — using shared audio from MiniPlayer */}

      {/* Background glow that pulses when playing */}
      <div
        className={`absolute inset-0 bg-gradient-to-br from-primary-container/5 to-transparent transition-opacity duration-1000 ${isPlaying ? "opacity-100" : "opacity-0"}`}
      />

      <div className="flex flex-col md:flex-row gap-6 items-center relative z-10">
        {/* Album Art */}
        <div className="relative w-40 h-40 flex-shrink-0 group">
          <div className={`absolute inset-0 bg-gradient-to-br from-primary-container to-secondary rounded-lg transition-transform duration-500 ${isPlaying ? "rotate-6 scale-105" : "rotate-3"}`} />
          <div className="relative w-full h-full bg-surface-container-highest rounded-lg shadow-lg flex items-center justify-center overflow-hidden">
            {/* Vinyl disc that spins when playing */}
            <div className={`w-28 h-28 rounded-full border-[12px] border-surface-container-lowest flex items-center justify-center ${isPlaying ? "animate-spin-slow" : ""}`}>
              <div className="w-8 h-8 rounded-full bg-primary-container/40 border-4 border-surface-container-lowest" />
            </div>
            {/* Equalizer overlay when playing */}
            <div className={`absolute bottom-3 left-1/2 -translate-x-1/2 flex items-end gap-[3px] transition-opacity duration-300 ${isPlaying ? "opacity-100" : "opacity-0"}`}>
              {[1, 2, 3, 4, 3, 2, 1].map((_, i) => (
                <div key={i} className={`eq-bar eq-bar-${(i % 4) + 1} bg-primary w-[3px]`} style={{ height: "14px" }} />
              ))}
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="flex-1 space-y-4 w-full">
          <div>
            <h4 className={`text-2xl md:text-3xl font-bold tracking-tight ${isPlaying ? "animate-text-glow" : ""}`}>
              {title}
            </h4>
          </div>

          {/* Waveform Visualization */}
          <div className="h-16 flex items-end gap-[2px] px-1 cursor-pointer" onClick={seek}>
            {waveformBars.map((h, i) => {
              const barProgress = (i / waveformBars.length) * 100;
              const isPast = barProgress < progress;
              const isCurrent = Math.abs(barProgress - progress) < 3;
              return (
                <div
                  key={i}
                  className={`flex-1 rounded-full transition-all duration-150 ${
                    isPast ? "bg-primary" :
                    isCurrent ? "bg-primary shadow-[0_0_8px_rgba(249,115,22,0.5)]" :
                    "bg-primary/20"
                  } ${isPlaying && isCurrent ? "animate-pulse" : ""}`}
                  style={{
                    height: `${h}%`,
                    transform: isPlaying && isCurrent ? "scaleY(1.2)" : "scaleY(1)",
                    transition: "height 0.3s, transform 0.15s, background-color 0.15s",
                  }}
                />
              );
            })}
          </div>

          {/* Time display */}
          <div className="flex justify-between text-[10px] font-bold text-on-surface-variant/60 tracking-tighter tabular-nums px-1">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(totalDuration)}</span>
          </div>

          {/* Playback Controls */}
          <div className="flex items-center gap-6 pt-1">
            <button className="material-symbols-outlined text-on-surface-variant/40 hover:text-primary transition-colors text-xl">
              skip_previous
            </button>
            <button
              onClick={togglePlay}
              className={`w-14 h-14 rounded-full bg-primary-container text-on-primary flex items-center justify-center shadow-lg hover:scale-110 active:scale-95 transition-all duration-300 ${isPlaying ? "play-btn-active" : ""}`}
            >
              <span
                className="material-symbols-outlined text-3xl"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                {isPlaying ? "pause" : "play_arrow"}
              </span>
            </button>
            <button className="material-symbols-outlined text-on-surface-variant/40 hover:text-primary transition-colors text-xl">
              skip_next
            </button>
            <div className="flex-1" />
            <button className="material-symbols-outlined text-on-surface-variant/40 hover:text-primary transition-colors text-xl">
              favorite
            </button>
            <button
              onClick={async () => {
                const url = storyId ? `${window.location.origin}/story/${storyId}` : window.location.href;
                const shareData = { title: `Voiceless: ${title}`, text: `Listen to "${title}" on Voiceless`, url };
                try {
                  if (navigator.share) {
                    await navigator.share(shareData);
                  } else {
                    await navigator.clipboard.writeText(url);
                    setShared(true);
                    setTimeout(() => setShared(false), 2000);
                  }
                } catch {
                  // user cancelled share dialog
                }
              }}
              className={`material-symbols-outlined text-xl transition-colors ${shared ? "text-primary" : "text-on-surface-variant/40 hover:text-primary"}`}
            >
              {shared ? "check" : "share"}
            </button>
          </div>
        </div>
      </div>

      {/* Story text with karaoke-style reveal */}
      {text && (
        <div className="mt-6 bg-surface-container-lowest/80 rounded-lg p-5 max-h-48 overflow-y-auto border border-outline-variant/10">
          <p className="text-sm leading-relaxed italic">
            <span className="text-on-surface">&ldquo;{text.slice(0, revealedLength)}</span>
            <span className="text-on-surface-variant/20">{text.slice(revealedLength, 500)}{text.length > 500 ? "..." : ""}</span>
            <span className="text-on-surface">&rdquo;</span>
          </p>
          {!isPlaying && progress === 0 && (
            <p className="text-on-surface-variant/30 text-xs mt-2 flex items-center gap-1">
              <span className="material-symbols-outlined text-sm">play_arrow</span>
              Press play to reveal the story
            </p>
          )}
        </div>
      )}
    </div>
  );
}
