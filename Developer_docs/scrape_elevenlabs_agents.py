"""
ElevenLabs Agents Docs Scraper
================================
Scrapes 31 essential ElevenAgents pages and saves them
as clean markdown files in elevenlabs_agents/
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
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "elevenlabs_agents")

EXCLUDE_TAGS = ["nav", "footer", "header", "aside", ".sidebar", ".breadcrumb", ".pagination"]

TARGET_URLS = [
    # ── Foundation ──────────────────────────────
    "https://elevenlabs.io/docs/eleven-agents/overview",
    "https://elevenlabs.io/docs/eleven-agents/quickstart",
    "https://elevenlabs.io/docs/eleven-agents/build/overview",
    "https://elevenlabs.io/docs/eleven-agents/dashboard",

    # ── Customization ───────────────────────────
    "https://elevenlabs.io/docs/eleven-agents/customization/agent-workflows",
    "https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow",
    "https://elevenlabs.io/docs/eleven-agents/customization/authentication",
    "https://elevenlabs.io/docs/eleven-agents/customization/tools",
    "https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools",
    "https://elevenlabs.io/docs/eleven-agents/customization/tools/server-tools",
    "https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools",
    "https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp",
    "https://elevenlabs.io/docs/eleven-agents/customization/knowledge-base",
    "https://elevenlabs.io/docs/eleven-agents/customization/knowledge-base/rag",
    "https://elevenlabs.io/docs/eleven-agents/customization/llm",
    "https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm",
    "https://elevenlabs.io/docs/eleven-agents/customization/llm/optimizing-costs",
    "https://elevenlabs.io/docs/eleven-agents/customization/personalization",
    "https://elevenlabs.io/docs/eleven-agents/customization/personalization/dynamic-variables",
    "https://elevenlabs.io/docs/eleven-agents/customization/events",
    "https://elevenlabs.io/docs/eleven-agents/customization/events/client-to-server-events",
    "https://elevenlabs.io/docs/eleven-agents/customization/widget",
    "https://elevenlabs.io/docs/eleven-agents/customization/agent-testing",
    "https://elevenlabs.io/docs/eleven-agents/customization/agent-analysis",

    # ── Best Practices ──────────────────────────
    "https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide",
    "https://elevenlabs.io/docs/eleven-agents/best-practices/guardrails",

    # ── Libraries / SDKs ────────────────────────
    "https://elevenlabs.io/docs/eleven-agents/libraries/python",
    "https://elevenlabs.io/docs/eleven-agents/libraries/java-script",
    "https://elevenlabs.io/docs/eleven-agents/libraries/web-sockets",

    # ── Deploy & Operate ────────────────────────
    "https://elevenlabs.io/docs/eleven-agents/integrate/overview",
    "https://elevenlabs.io/docs/eleven-agents/operate/overview",

    # ── Phone & Messaging ───────────────────────
    "https://elevenlabs.io/docs/eleven-agents/phone-numbers/batch-calls",
    "https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration",

    # ── Workflows ───────────────────────────────
    "https://elevenlabs.io/docs/eleven-agents/workflows/post-call-webhooks",
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
    path = url.replace("https://elevenlabs.io/docs/eleven-agents/", "").strip("/")
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

        if stripped in ("Skip to main content", "Search...", "Ctrl K", "Copy", "Was this page helpful?"):
            continue
        if re.match(r"^(Yes|No|Previous|Next)$", stripped):
            continue
        if re.match(r"^(Docs\s*[>»]|Navigation$)", stripped):
            continue
        if re.match(r"^!\[.*?\]\(https://mintcdn\.com/.*\)$", stripped):
            continue

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

    print("\nTarget pages (ElevenAgents):")
    for i, url in enumerate(TARGET_URLS, 1):
        path = url.replace("https://elevenlabs.io/docs/eleven-agents/", "")
        print(f"  {i:>2}. {path}")

    print(f"\nTotal: {len(TARGET_URLS)} pages (~{len(TARGET_URLS) + 1} credits)")
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    scrape(fc)


if __name__ == "__main__":
    main()
