"""Gemini API wrapper — price analysis, currency conversion, visual identification."""

import base64
import json
import logging

from google import genai
from google.genai import types

from config import GEMINI_API_KEY

log = logging.getLogger(__name__)

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


MODEL = "gemini-2.5-flash"


async def _ask(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    client = _get_client()
    try:
        resp = client.models.generate_content(model=MODEL, contents=prompt)
        return resp.text or ""
    except Exception as e:
        log.error("Gemini call failed: %s", e)
        return ""


def _parse_json(text: str) -> dict | list | None:
    """Best-effort parse JSON from Gemini response (handles markdown fences)."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:])
        if text.endswith("```"):
            text = text[:-3]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        # Try to find JSON within the text
        for start_char, end_char in [("{", "}"), ("[", "]")]:
            start = text.find(start_char)
            end = text.rfind(end_char)
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    continue
        return None


async def analyze_prices(results: list[dict], product_query: str, region: str, currency: str) -> dict:
    """Analyze verified price results and return a recommendation."""
    prompt = f"""You are a shopping expert. Analyze these verified prices for "{product_query}" in region {region} (currency {currency}).

Each result has a trust_score (0-100), condition (new/refurbished), warnings, and seller_type.
Prioritize deals that are: in-stock, new condition, high trust_score, from official/trusted sellers.
Do NOT recommend a deal with trust_score < 40 or with serious warnings, even if it's the cheapest.

Results:
{json.dumps(results, indent=2)}

Respond ONLY with a JSON object (no markdown fences):
{{
  "best_deal_index": <index of best TRUSTWORTHY deal>,
  "recommendation": "<2-3 sentence recommendation factoring in price, trust, and condition>",
  "buy_now_or_wait": "buy_now" or "wait",
  "confidence": "high" or "medium" or "low",
  "warnings": ["<any deal-specific warnings the user should know>"]
}}"""
    raw = await _ask(prompt)
    parsed = _parse_json(raw)
    if isinstance(parsed, dict):
        return parsed
    return {
        "best_deal_index": 0,
        "recommendation": "Based on current prices, the top result appears to be the best available deal.",
        "buy_now_or_wait": "buy_now",
        "confidence": "low",
        "warnings": [],
    }


async def estimate_cross_border_cost(
    price: float, from_currency: str, to_currency: str, product_category: str = "electronics"
) -> dict:
    """Estimate total landed cost for a cross-border purchase."""
    prompt = f"""Convert {price} {from_currency} to {to_currency} at current approximate exchange rates.
Product category: {product_category}.
Estimate import duty/tax for a buyer in a {to_currency} country.
Estimate international shipping cost range.

Respond ONLY with a JSON object (no markdown fences):
{{
  "converted_price": <number>,
  "import_duty_estimate": <number>,
  "shipping_estimate_low": <number>,
  "shipping_estimate_high": <number>,
  "total_estimate_low": <number>,
  "total_estimate_high": <number>,
  "exchange_rate_note": "<brief note>"
}}"""
    raw = await _ask(prompt)
    parsed = _parse_json(raw)
    if isinstance(parsed, dict):
        return parsed
    return {"converted_price": price, "import_duty_estimate": 0, "total_estimate_low": price, "total_estimate_high": price}


async def verify_deal(
    product_query: str,
    scraped_price: float,
    scraped_currency: str,
    original_price: float | None,
    page_markdown: str,
) -> dict:
    """Verify if a scraped deal is legitimate by analyzing the full page content.

    Catches: variant bait-and-switch, conditional pricing, refurbished mixing,
    MRP inflation, hidden fees, seller risk, stock tricks.

    Returns dict with trust_score (0-100), warnings, verified_price, condition.
    """
    # Truncate markdown to fit context window
    md_truncated = page_markdown[:6000] if page_markdown else "(no page content available)"

    prompt = f"""You are a deal verification expert protecting consumers from deceptive pricing.

A scraper extracted this price for "{product_query}":
- Scraped price: {scraped_price} {scraped_currency}
- Original/MRP: {original_price or "not found"}

Below is the raw page content. Analyze it for these 7 deception patterns:

1. VARIANT BAIT: Is {scraped_price} {scraped_currency} for the EXACT product "{product_query}", or is it for a cheaper variant (wrong storage, wired vs wireless, smaller size, different color at different price)?
2. CONDITIONAL PRICE: Does getting {scraped_price} require a bank card offer, exchange/trade-in, coupon code, first-time user status, or membership?
3. REFURBISHED MIX: Is this for a BRAND NEW unit, or refurbished/renewed/open-box/used?
4. MRP INFLATION: Is the "original price" {original_price} realistic for this product, or is it artificially inflated to fake a bigger discount?
5. HIDDEN FEES: Are there delivery/shipping charges, handling fees, platform fees, or taxes NOT included in {scraped_price}?
6. SELLER RISK: On marketplace sites, is this from the official brand store or a trusted seller, or an unknown third-party?
7. STOCK TRICK: Does the page indicate "out of stock", "currently unavailable", "notify me", or "coming soon" despite showing a price?

Page content:
{md_truncated}

Respond ONLY with a JSON object (no markdown fences):
{{
  "trust_score": <0-100, where 100 = fully verified legitimate deal>,
  "verified_price": <the actual price a normal buyer would pay, or null if uncertain>,
  "condition": "new" or "refurbished" or "open_box" or "unknown",
  "is_correct_product": true or false,
  "price_requires_conditions": true or false,
  "conditions": ["list of conditions needed for this price, if any"],
  "hidden_costs": ["list of additional costs found"],
  "seller_type": "official" or "trusted_third_party" or "unknown_seller" or "marketplace_mix",
  "warnings": ["short description of each deception pattern found"],
  "adjusted_reason": "<if verified_price differs from scraped price, explain why>"
}}"""

    raw = await _ask(prompt)
    parsed = _parse_json(raw)
    if isinstance(parsed, dict):
        return parsed
    return {
        "trust_score": 50,
        "verified_price": None,
        "condition": "unknown",
        "is_correct_product": True,
        "price_requires_conditions": False,
        "conditions": [],
        "hidden_costs": [],
        "seller_type": "unknown",
        "warnings": ["Could not verify — treat with caution"],
        "adjusted_reason": "",
    }


async def extract_coupon_codes(search_texts: list[str]) -> list[str]:
    """Extract coupon/promo codes from scraped text snippets."""
    prompt = f"""Extract all valid-looking coupon or promo codes from these texts:

{json.dumps(search_texts)}

Return ONLY a JSON array of code strings (4-20 alphanumeric characters, typically ALLCAPS).
Ignore generic words. Example: ["SAVE15", "TECH20", "FLAT500"]
If none found, return [].
"""
    raw = await _ask(prompt)
    parsed = _parse_json(raw)
    if isinstance(parsed, list):
        return [str(c) for c in parsed if isinstance(c, str) and 3 <= len(c) <= 25]
    return []


async def identify_product(image_b64: str, mime_type: str = "image/jpeg") -> dict:
    """Identify a product from a camera image using Gemini vision.

    Returns dict with product_name, brand, model, category, confidence, variants, search_query.
    """
    client = _get_client()
    image_bytes = base64.b64decode(image_b64)

    prompt = """You are a product identification expert. Identify the product in this image.

Look for:
- Brand name and logo
- Model number (on the product body, packaging, or label)
- Product category (headphones, phone, laptop, etc.)
- Color and any visible variant info (storage size, edition)

Respond ONLY with a JSON object (no markdown fences):
{
  "identified": true or false,
  "confidence": "high" or "medium" or "low",
  "brand": "<brand name>",
  "model": "<specific model name/number>",
  "product_name": "<full product name for search, e.g. Sony WH-1000XM5>",
  "category": "<product category>",
  "color": "<color if visible>",
  "variants": ["<possible variants if model is ambiguous, e.g. 128GB, 256GB>"],
  "search_query": "<optimized search query to find this product's price>",
  "ambiguity_note": "<if confidence is low/medium, explain what's uncertain>"
}

If you cannot identify the product at all, set identified=false and explain in ambiguity_note."""

    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt,
            ],
        )
        raw = resp.text or ""
    except Exception as e:
        log.error("Gemini vision call failed: %s", e)
        return {"identified": False, "confidence": "low", "ambiguity_note": str(e)}

    parsed = _parse_json(raw)
    if isinstance(parsed, dict):
        return parsed
    return {"identified": False, "confidence": "low", "ambiguity_note": "Failed to parse response"}
