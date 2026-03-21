"""Gemini API wrapper — price analysis, currency conversion, recommendations."""

import json
import logging

from google import genai

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
    """Analyze a list of price results and return a recommendation."""
    prompt = f"""You are a shopping expert. Analyze these prices for "{product_query}" in region {region} (currency {currency}).

Results:
{json.dumps(results, indent=2)}

Respond ONLY with a JSON object (no markdown fences):
{{
  "best_deal_index": <index of best deal in the list>,
  "recommendation": "<1-2 sentence recommendation: buy now or wait, and why>",
  "buy_now_or_wait": "buy_now" or "wait",
  "confidence": "high" or "medium" or "low",
  "warnings": ["<any scam/fake review warnings>"]
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
