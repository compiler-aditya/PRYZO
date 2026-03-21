"""Firecrawl SDK wrapper — Search, Scrape, Browser Sandbox."""

import json
import logging
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from firecrawl import Firecrawl
from firecrawl.v2.types import JsonFormat

from config import FIRECRAWL_API_KEY

log = logging.getLogger(__name__)

_client: Firecrawl | None = None


def _get_client() -> Firecrawl:
    global _client
    if _client is None:
        _client = Firecrawl(api_key=FIRECRAWL_API_KEY)
    return _client


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SearchHit:
    url: str
    title: str
    description: str
    domain: str
    snippet_price: float | None = None
    snippet_currency: str | None = None
    needs_scrape: bool = True


@dataclass
class ScrapedPrice:
    url: str
    domain: str
    product_name: str
    price: float
    currency: str
    in_stock: bool = True
    shipping_cost: float | None = None
    original_price: float | None = None
    discount_pct: float | None = None


# ---------------------------------------------------------------------------
# Price extraction from search snippets (Tier 1 — FREE, no extra credits)
# ---------------------------------------------------------------------------

_PRICE_PATTERNS = [
    # ₹24,990 or Rs 24,990 or Rs. 24990 or INR 24,990
    (r"(?:₹|Rs\.?\s*|INR\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "INR"),
    # $299.99 or USD 299
    (r"(?:\$|USD\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "USD"),
    # £199.99 or GBP 199
    (r"(?:£|GBP\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "GBP"),
    # €199.99 or EUR 199
    (r"(?:€|EUR\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "EUR"),
    # ¥29,800 or JPY 29800
    (r"(?:¥|JPY\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "JPY"),
    # A$399 or AUD 399
    (r"(?:A\$|AUD\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "AUD"),
    # C$399 or CAD 399
    (r"(?:C\$|CAD\s*)([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?)", "CAD"),
]


def extract_price_from_text(text: str) -> tuple[float | None, str | None]:
    """Try to extract a price and currency from a snippet of text."""
    if not text:
        return None, None
    for pattern, currency in _PRICE_PATTERNS:
        m = re.search(pattern, text)
        if m:
            price_str = m.group(1).replace(",", "")
            try:
                return float(price_str), currency
            except ValueError:
                continue
    return None, None


def extract_domain(url: str) -> str:
    """Return the bare domain from a URL (e.g., 'www.amazon.in' → 'amazon.in')."""
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


# ---------------------------------------------------------------------------
# Tier 1 — Firecrawl Search
# ---------------------------------------------------------------------------

async def search_products(query: str, location: str, limit: int = 10) -> list[SearchHit]:
    """Run a Firecrawl web search with geo-targeting. Returns parsed hits."""
    fc = _get_client()
    # Include location in query to improve regional relevance
    search_query = f"{query} price buy online in {location}"
    try:
        results = fc.search(
            query=search_query,
            limit=limit,
            location=location,
        )
    except Exception as e:
        log.error("Firecrawl search failed: %s", e)
        return []

    hits: list[SearchHit] = []

    # SearchData has .web, .news, .images attributes
    data = getattr(results, "web", None)
    if data is None:
        data = results if isinstance(results, list) else getattr(results, "data", results)
        if isinstance(data, dict):
            data = data.get("web", data.get("data", []))

    for item in data or []:
        if isinstance(item, dict):
            url = item.get("url", "")
            title = item.get("title", "")
            desc = item.get("description", "")
        else:
            url = getattr(item, "url", "")
            title = getattr(item, "title", "")
            desc = getattr(item, "description", "")

        if not url:
            continue

        domain = extract_domain(url)
        combined_text = f"{title} {desc}"
        price, currency = extract_price_from_text(combined_text)

        hits.append(SearchHit(
            url=url,
            title=title,
            description=desc,
            domain=domain,
            snippet_price=price,
            snippet_currency=currency,
            needs_scrape=price is None,
        ))

    return hits


# ---------------------------------------------------------------------------
# Tier 2 — Targeted Scrape with JSON schema
# ---------------------------------------------------------------------------

PRICE_SCHEMA = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number"},
        "currency": {"type": "string"},
        "in_stock": {"type": "boolean"},
        "shipping_cost": {"type": "number"},
        "original_price": {"type": "number"},
        "discount_percentage": {"type": "number"},
    },
    "required": ["product_name", "price", "currency"],
}


async def scrape_product_page(url: str) -> ScrapedPrice | None:
    """Scrape a single product page and extract structured price data. 1 credit."""
    fc = _get_client()
    try:
        result = fc.scrape(
            url=url,
            formats=[JsonFormat(
                type="json",
                schema=PRICE_SCHEMA,
                prompt="Extract the main product's current selling price, currency, stock status, and shipping cost.",
            )],
        )
    except Exception as e:
        log.error("Firecrawl scrape failed for %s: %s", url, e)
        return None

    # Parse the structured response
    json_data = None
    if isinstance(result, dict):
        json_data = result.get("json") or result.get("data", {}).get("json")
    else:
        json_data = getattr(result, "json", None)
        if json_data is None:
            data_obj = getattr(result, "data", None)
            if data_obj:
                json_data = getattr(data_obj, "json", None) or (data_obj.get("json") if isinstance(data_obj, dict) else None)

    if not json_data:
        # Fallback: try extracting from markdown
        md = ""
        if isinstance(result, dict):
            md = result.get("markdown", "")
        else:
            md = getattr(result, "markdown", "") or ""
        price, currency = extract_price_from_text(md)
        if price:
            return ScrapedPrice(
                url=url,
                domain=extract_domain(url),
                product_name="",
                price=price,
                currency=currency or "USD",
            )
        return None

    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            return None

    price_val = json_data.get("price")
    if price_val is None:
        return None

    # Normalize currency symbols to codes
    raw_currency = json_data.get("currency", "USD")
    _SYMBOL_TO_CODE = {"₹": "INR", "$": "USD", "£": "GBP", "€": "EUR", "¥": "JPY"}
    currency_code = _SYMBOL_TO_CODE.get(raw_currency, raw_currency)

    return ScrapedPrice(
        url=url,
        domain=extract_domain(url),
        product_name=json_data.get("product_name", ""),
        price=float(price_val),
        currency=currency_code,
        in_stock=json_data.get("in_stock", True),
        shipping_cost=json_data.get("shipping_cost"),
        original_price=json_data.get("original_price"),
        discount_pct=json_data.get("discount_percentage"),
    )
