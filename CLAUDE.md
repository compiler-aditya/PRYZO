# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

PRYZO is a **documentation knowledge base** for the ElevenHacks hackathon — a competition to build something unique using both **Firecrawl** (web scraping/search API) and **ElevenLabs ElevenAgents** (conversational voice agents platform). The repo contains scraped reference docs and scraper scripts; no application code exists yet.

- `elvenhacks.md` — Hackathon rules, scoring criteria, and submission guidelines
- `Developer_docs/` — All scraped reference documentation

## Repository Structure

```
Developer_docs/
├── elevenlabs_agents/       # ElevenAgents platform docs (31 pages): workflows, tools, SDKs, deployment
├── elevenlabs_docs/         # ElevenLabs API docs (20 pages): TTS, STT, voice cloning, models
├── elevenlabs_dev_journey/  # Developer journey docs (20 pages): auth → TTS → streaming → WebSockets
├── docs.firecrawl.dev/      # Firecrawl docs: scraping, search, crawl, map, agent, browser sandbox
├── Developer_guides/        # Firecrawl developer guides and cookbooks
├── UseCases/                # Firecrawl use case docs (AI platforms, deep research, lead enrichment, etc.)
├── Webhooks/                # Firecrawl webhook docs (events, security, testing)
├── elevenlabs_url_index.md  # Index of 705 ElevenLabs doc URLs
├── enrichment_results.csv   # Firecrawl enrichment metadata
├── scrape_elevenlabs_agents.py    # Scraper for ElevenAgents docs
├── scrape_elevenlabs_docs.py      # Scraper for ElevenLabs API docs
└── scrape_elevenlabs_dev_journey.py  # Scraper for developer journey docs
```

## Running the Scrapers

The three Python scrapers use the `firecrawl` Python SDK. They require:

```bash
pip install firecrawl
export FIRECRAWL_API_KEY="fc-YOUR-KEY"
python Developer_docs/scrape_elevenlabs_agents.py
```

Each scraper prompts for confirmation before proceeding. They attempt batch scraping first, falling back to sequential scraping on failure. Output goes to the corresponding subdirectory under `Developer_docs/`.

## Key APIs for Building

### Firecrawl
- **Search API** — `firecrawl.search(query, limit)` — web search with structured content in one call
- **Scrape API** — `firecrawl.scrape(url, formats=["markdown"])` — any URL to clean markdown/HTML/JSON
- **Agent** — autonomous web data gathering from a text prompt
- **Browser Sandbox** — managed browser sessions for form filling, clicking, authentication
- Python SDK: `from firecrawl import Firecrawl`
- Base URL: `https://api.firecrawl.dev/v2/`

### ElevenLabs ElevenAgents
- Conversational voice agents with ASR → LLM → TTS pipeline
- Architecture: fine-tuned STT, configurable LLM, low-latency TTS (5k+ voices, 70+ languages), proprietary turn-taking model
- Tools: server tools (API calls), client tools (browser-side actions), system tools (built-in), MCP
- SDKs: Python, JavaScript, React, Swift, Kotlin, React Native, WebSocket
- Widget embed: `<elevenlabs-convai agent-id="ID"></elevenlabs-convai>`
- Deploy via: web widget, phone (Twilio/SIP), batch outbound calls

### Environment Variables
- `FIRECRAWL_API_KEY` — required for Firecrawl API and scrapers
- `ELEVENLABS_API_KEY` — required for ElevenLabs API (when building the project)

## Doc File Naming Conventions

- ElevenLabs docs use `__` as path separators (e.g., `customization__tools__server-tools.md`)
- Firecrawl docs use the full URL path as the filename with timestamps
- Each scraped doc starts with a `<!-- Source: URL -->` comment linking to the original page
