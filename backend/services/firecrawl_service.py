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

# Patterns that indicate a price is NOT a product price — skip these
_JUNK_PRICE_CONTEXT = re.compile(
    r"(?:per\s*month|/mo(?:nth)?|emi|instalment|installment|starting\s*(?:from|at)"
    r"|price\s*history|lowest\s*price\s*was|was\s*₹|was\s*\$|was\s*£|was\s*€"
    r"|cashback|reward|(?:up\s*to|save)\s*(?:₹|Rs|USD|\$|£|€))",
    re.IGNORECASE,
)

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

# Currency symbol → code mapping for normalization
_SYMBOL_TO_CODE = {"₹": "INR", "$": "USD", "£": "GBP", "€": "EUR", "¥": "JPY"}


def extract_price_from_text(text: str) -> tuple[float | None, str | None]:
    """Try to extract a valid product price from text.

    Skips EMI prices, cashback, price history, and "starting from" patterns.
    """
    if not text:
        return None, None

    for pattern, currency in _PRICE_PATTERNS:
        m = re.search(pattern, text)
        if not m:
            continue

        # Check context around the match — is this junk?
        start = max(0, m.start() - 40)
        end = min(len(text), m.end() + 20)
        context = text[start:end]
        if _JUNK_PRICE_CONTEXT.search(context):
            continue

        price_str = m.group(1).replace(",", "")
        try:
            price = float(price_str)
        except ValueError:
            continue

        # Sanity: ignore suspiciously small prices (likely page numbers, ratings, etc.)
        if price < 10:
            continue

        return price, currency

    return None, None


# ---------------------------------------------------------------------------
# URL / Domain helpers
# ---------------------------------------------------------------------------

# Non-retailer domains — review sites, comparison engines, forums, blogs
_NON_RETAILER_DOMAINS = frozenset({
    "camelcamelcamel.com", "pricehistory.app", "pricebefore.com",
    "pricespy.co.uk", "idealo.de", "geizhals.de", "skinflint.co.uk",
    "reddit.com", "quora.com", "youtube.com", "twitter.com",
    "facebook.com", "instagram.com", "pinterest.com",
    "gsmarena.com", "rtings.com", "techradar.com", "tomsguide.com",
    "verge.com", "theverge.com", "cnet.com", "pcmag.com",
    "gadgets360.com", "91mobiles.com", "smartprix.com", "pricebaba.com",
    "mysmartprice.com", "news18.com", "ndtv.com",
    "wikipedia.org", "wikihow.com",
    "klarna.com", "afterpay.com", "paypal.com",
    "unboxify.in", "designinfo.in", "compareraja.in",
})

# URL path patterns that indicate non-product pages
_NON_PRODUCT_PATH = re.compile(
    r"/(?:blog|article|review|compare|versus|vs|news|guide|how-to|best-|top-\d+)",
    re.IGNORECASE,
)


def extract_domain(url: str) -> str:
    """Return the bare domain from a URL (e.g., 'www.amazon.in' → 'amazon.in')."""
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def extract_base_domain(domain: str) -> str:
    """Strip subdomain to get base domain (e.g., 'luxury.tatacliq.com' → 'tatacliq.com').

    Handles multi-part TLDs like .co.uk, .co.jp, .com.au.
    """
    parts = domain.split(".")
    # Known multi-part TLDs
    multi_tlds = {"co.uk", "co.jp", "com.au", "co.in", "co.nz", "com.br", "co.kr"}
    if len(parts) >= 3:
        last_two = f"{parts[-2]}.{parts[-1]}"
        if last_two in multi_tlds:
            # base domain = x.co.uk
            return ".".join(parts[-3:])
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return domain


def is_product_url(url: str, domain: str) -> bool:
    """Return True if this URL is likely a product page, not a review/blog/comparison."""
    base = extract_base_domain(domain)
    if base in _NON_RETAILER_DOMAINS:
        return False
    path = urlparse(url).path
    if _NON_PRODUCT_PATH.search(path):
        return False
    return True


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

        # Skip non-product URLs (reviews, blogs, comparison sites)
        if not is_product_url(url, domain):
            log.debug("Skipping non-product URL: %s", url)
            continue

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
        "price": {"type": "number", "description": "Current selling price (not EMI, not MRP)"},
        "currency": {"type": "string"},
        "in_stock": {"type": "boolean"},
        "shipping_cost": {"type": "number"},
        "original_price": {"type": "number", "description": "MRP or list price before discount"},
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
                prompt=(
                    "Extract the main product's CURRENT SELLING PRICE (not EMI, not MRP/list price). "
                    "Include currency, stock status, shipping cost, and original price if discounted."
                ),
            )],
            timeout=15000,  # 15s timeout
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

    try:
        price_float = float(price_val)
    except (TypeError, ValueError):
        return None

    # Sanity: skip absurdly small prices
    if price_float < 10:
        return None

    # Normalize currency symbols to codes
    raw_currency = json_data.get("currency", "USD")
    currency_code = _SYMBOL_TO_CODE.get(raw_currency, raw_currency)

    return ScrapedPrice(
        url=url,
        domain=extract_domain(url),
        product_name=json_data.get("product_name", ""),
        price=price_float,
        currency=currency_code,
        in_stock=json_data.get("in_stock", True),
        shipping_cost=json_data.get("shipping_cost"),
        original_price=json_data.get("original_price"),
        discount_pct=json_data.get("discount_percentage"),
    )
