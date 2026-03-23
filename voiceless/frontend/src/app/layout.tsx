import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import Link from "next/link";
import Script from "next/script";
import MiniPlayer from "@/components/MiniPlayer";
import "./globals.css";

const jakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-jakarta",
  weight: ["300", "400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Voiceless — Every story matters. No name needed.",
  description:
    "An anonymous storytelling platform where human stories are produced as intimate audio experiences.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
        <meta name="theme-color" content="#0b1326" />
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
          rel="stylesheet"
        />
        <Script
          src="https://unpkg.com/@elevenlabs/convai-widget-embed"
          strategy="lazyOnload"
        />
      </head>
      <body
        className={`${jakarta.variable} font-sans antialiased bg-surface text-on-surface min-h-screen`}
      >
        <div className="grain-overlay" />

        {/* Header */}
        <header className="w-full top-0 z-50 bg-gradient-to-b from-surface-container-low to-transparent sticky">
          <div className="flex justify-between items-center px-4 md:px-6 py-3 md:py-4 max-w-[1600px] mx-auto">
            <Link href="/" className="flex items-center gap-2 md:gap-3 group">
              <span className="material-symbols-outlined text-primary-container text-2xl md:text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
                mic
              </span>
              <span className="text-lg md:text-2xl font-extrabold tracking-tight text-primary-container uppercase">
                voiceless
              </span>
            </Link>

            <nav className="hidden md:flex bg-surface-container-low p-1.5 rounded-full items-center gap-1">
              <Link
                href="/"
                className="px-6 py-1.5 text-primary font-bold text-sm hover:text-secondary transition-colors duration-300"
              >
                Stories
              </Link>
              <Link
                href="/moments"
                className="px-6 py-1.5 text-on-surface-variant text-sm hover:text-secondary transition-colors duration-300"
              >
                Moments
              </Link>
              <Link
                href="/submit"
                className="px-6 py-1.5 text-on-surface-variant text-sm hover:text-secondary transition-colors duration-300"
              >
                Share
              </Link>
            </nav>

            <div className="flex items-center gap-2 md:gap-4">
              <button className="material-symbols-outlined text-on-surface-variant hover:text-secondary transition-colors duration-300 p-2">
                search
              </button>
            </div>
          </div>
        </header>

        {/* Main content — extra bottom padding on mobile for nav bar + footer stack */}
        <main className="max-w-[1200px] mx-auto px-4 md:px-6 py-4 md:py-8 pb-36 md:pb-20">
          {children}
        </main>

        {/* Mini Player */}
        <MiniPlayer />

        {/* Footer Identity Strip — hidden on mobile to save space */}
        <footer className="hidden md:flex w-full py-2.5 bg-primary-container justify-center items-center fixed bottom-0 z-40">
          <div className="flex flex-row justify-center items-center gap-8 px-6">
            <span className="text-[10px] font-extrabold uppercase tracking-[0.2em] text-on-primary">
              The Identity Promise
            </span>
            <div className="h-1 w-1 bg-on-primary rounded-full" />
            <p className="text-[10px] font-bold uppercase tracking-widest text-on-primary/80">
              Your story, your voice, never your name
            </p>
          </div>
        </footer>

        {/* Mobile Nav Bar — sits at the very bottom */}
        <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-surface-container-highest/95 backdrop-blur-xl px-6 py-2 pb-[max(0.5rem,env(safe-area-inset-bottom))] flex justify-around items-center shadow-2xl z-50 border-t border-outline-variant/10">
          <Link href="/" className="flex flex-col items-center gap-0.5 py-1 min-w-[48px]">
            <span className="material-symbols-outlined text-primary text-[22px]" style={{ fontVariationSettings: "'FILL' 1" }}>home</span>
            <span className="text-[9px] font-bold text-primary">Home</span>
          </Link>
          <Link href="/moments" className="flex flex-col items-center gap-0.5 py-1 min-w-[48px]">
            <span className="material-symbols-outlined text-on-surface-variant text-[22px]">explore</span>
            <span className="text-[9px] font-medium text-on-surface-variant/60">Moments</span>
          </Link>
          <Link
            href="/submit"
            className="w-14 h-14 bg-primary-container rounded-full -mt-7 flex items-center justify-center shadow-lg shadow-primary-container/30 border-4 border-surface active:scale-90 transition-transform"
          >
            <span className="material-symbols-outlined text-on-primary text-2xl">mic</span>
          </Link>
          <Link href="/moments" className="flex flex-col items-center gap-0.5 py-1 min-w-[48px]">
            <span className="material-symbols-outlined text-on-surface-variant text-[22px]">notifications</span>
            <span className="text-[9px] font-medium text-on-surface-variant/60">Updates</span>
          </Link>
          <Link href="/submit" className="flex flex-col items-center gap-0.5 py-1 min-w-[48px]">
            <span className="material-symbols-outlined text-on-surface-variant text-[22px]">person</span>
            <span className="text-[9px] font-medium text-on-surface-variant/60">Profile</span>
          </Link>
        </nav>
      </body>
    </html>
  );
}
