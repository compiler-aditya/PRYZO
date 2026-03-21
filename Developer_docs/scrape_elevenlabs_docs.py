"""
ElevenLabs API Docs Scraper
============================
Scrapes 20 hand-picked pages covering ElevenLabs API capabilities
and saves each as a clean markdown file.
"""

import os
import re
import sys
import time
from firecrawl import Firecrawl

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────
API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "elevenlabs_docs")

EXCLUDE_TAGS = ["nav", "footer", "header", "aside", ".sidebar", ".breadcrumb", ".pagination"]

# ──────────────────────────────────────────────
# 20 most important pages for API developers
# ──────────────────────────────────────────────
TARGET_URLS = [
    # Platform foundation
    "https://elevenlabs.io/docs/overview/intro",
    "https://elevenlabs.io/docs/overview/models",
    "https://elevenlabs.io/docs/eleven-api/quickstart",
    "https://elevenlabs.io/docs/eleven-api/choosing-the-right-model",
    "https://elevenlabs.io/docs/api-reference/introduction",

    # Core capabilities
    "https://elevenlabs.io/docs/overview/capabilities/text-to-speech",
    "https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices",
    "https://elevenlabs.io/docs/overview/capabilities/speech-to-text",
    "https://elevenlabs.io/docs/overview/capabilities/voice-changer",
    "https://elevenlabs.io/docs/overview/capabilities/voices",
    "https://elevenlabs.io/docs/overview/capabilities/voice-cloning",
    "https://elevenlabs.io/docs/overview/capabilities/dubbing",
    "https://elevenlabs.io/docs/overview/capabilities/sound-effects",
    "https://elevenlabs.io/docs/overview/capabilities/music",
    "https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue",
    "https://elevenlabs.io/docs/overview/capabilities/voice-isolator",
    "https://elevenlabs.io/docs/overview/capabilities/forced-alignment",

    # Advanced / what can be built
    "https://elevenlabs.io/docs/eleven-agents/overview",
    "https://elevenlabs.io/docs/eleven-api/websockets",
    "https://elevenlabs.io/docs/eleven-api/resources/agent-tooling",
]


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def get_api_key() -> str:
    key = API_KEY
    if not key:
        key = input("Enter your FireCrawl API key (fc-...): ").strip()
        if not key:
            print("No API key provided. Exiting.")
            sys.exit(1)
    return key


def url_to_filename(url: str) -> str:
    path = url.replace("https://elevenlabs.io/docs", "").strip("/")
    if not path:
        return "index.md"
    filename = path.replace("/", "__") + ".md"
    filename = re.sub(r"[^\w.\-]", "_", filename)
    return filename


def clean_markdown(md: str, source_url: str) -> str:
    if not md:
        return ""

    lines = md.split("\n")
    cleaned = []
    prev_blank = False

    for line in lines:
        stripped = line.strip()

        # Strip UI boilerplate
        if stripped in ("Skip to main content", "Search...", "Ctrl K", "Copy", "Was this page helpful?"):
            continue
        if re.match(r"^(Yes|No|Previous|Next)$", stripped):
            continue
        if re.match(r"^(Docs\s*[>»]|Navigation$)", stripped):
            continue
        if re.match(r"^!\[.*?\]\(https://mintcdn\.com/.*\)$", stripped):
            continue

        # Collapse multiple blank lines
        if stripped == "":
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False

        cleaned.append(line)

    header = f"<!-- Source: {source_url} -->\n"
    body = "\n".join(cleaned).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)

    return header + "\n" + body + "\n"


# ──────────────────────────────────────────────
# Scrape
# ──────────────────────────────────────────────
def scrape(fc: Firecrawl) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = len(TARGET_URLS)

    print(f"\nScraping {total} pages → {OUTPUT_DIR}/\n")

    try:
        result = fc.batch_scrape(
            urls=TARGET_URLS,
            formats=["markdown"],
            only_main_content=True,
            exclude_tags=EXCLUDE_TAGS,
            poll_interval=3,
            wait_timeout=300,
        )
        docs = result.data
    except Exception as e:
        print(f"Batch scrape failed ({e}), falling back to sequential...\n")
        docs = None

    if docs:
        saved = 0
        for doc in docs:
            source_url = ""
            if doc.metadata:
                meta = doc.metadata if isinstance(doc.metadata, dict) else doc.metadata.model_dump()
                source_url = meta.get("sourceURL") or meta.get("source_url") or meta.get("url", "")

            if not source_url:
                continue

            filename = url_to_filename(source_url)
            content = clean_markdown(doc.markdown or "", source_url)

            if content.strip():
                with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                    f.write(content)
                saved += 1
                print(f"  [{saved}/{total}] {filename}")

        print(f"\nDone! Saved {saved}/{total} files to {OUTPUT_DIR}/")

    else:
        # Sequential fallback
        saved = 0
        for i, url in enumerate(TARGET_URLS, 1):
            try:
                doc = fc.scrape(url, formats=["markdown"], only_main_content=True, exclude_tags=EXCLUDE_TAGS)
                filename = url_to_filename(url)
                content = clean_markdown(doc.markdown or "", url)
                if content.strip():
                    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                        f.write(content)
                    saved += 1
                    print(f"  [{i}/{total}] {filename}")
                else:
                    print(f"  [{i}/{total}] Empty: {url}")
            except Exception as e:
                print(f"  [{i}/{total}] Error: {url} — {e}")
            if i < total:
                time.sleep(0.5)

        print(f"\nDone! Saved {saved}/{total} files to {OUTPUT_DIR}/")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    key = get_api_key()
    fc = Firecrawl(api_key=key)

    print("\nTarget pages:")
    for i, url in enumerate(TARGET_URLS, 1):
        path = url.replace("https://elevenlabs.io/docs", "")
        print(f"  {i:>2}. {path}")

    print(f"\nTotal: {len(TARGET_URLS)} pages (~{len(TARGET_URLS) + 1} credits)")
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    scrape(fc)


if __name__ == "__main__":
    main()
