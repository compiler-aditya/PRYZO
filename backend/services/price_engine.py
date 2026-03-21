"""Price Engine — 3-tier credit-efficient search orchestration."""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

from services import firecrawl_service as fc
from services import gemini_service as gem

log = logging.getLogger(__name__)

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "retailer_registry.json"

_registry: dict | None = None


def _load_registry() -> dict:
    global _registry
    if _registry is None:
        _registry = json.loads(REGISTRY_PATH.read_text())
    return _registry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@dataclass
class DealResult:
    retailer_name: str
    retailer_domain: str
    retailer_url: str
    price: float
    currency: str
    final_price: float
    original_price: float | None = None
    shipping_cost: float | None = None
    in_stock: bool = True
    coupon_code: str | None = None
    coupon_discount: float | None = None
    tier: int = 1
    is_cross_border: bool = False
    cross_border_total: float | None = None

    def to_dict(self) -> dict:
        return {
            "retailer_name": self.retailer_name,
            "retailer_domain": self.retailer_domain,
            "retailer_url": self.retailer_url,
            "price": self.price,
            "currency": self.currency,
            "final_price": self.final_price,
            "original_price": self.original_price,
            "shipping_cost": self.shipping_cost,
            "in_stock": self.in_stock,
            "coupon_code": self.coupon_code,
            "coupon_discount": self.coupon_discount,
            "tier": self.tier,
            "is_cross_border": self.is_cross_border,
            "cross_border_total": self.cross_border_total,
        }


@dataclass
class HuntResult:
    query: str
    region: str
    currency: str
    deals: list[DealResult] = field(default_factory=list)
    best_deal: dict | None = None
    runner_up: dict | None = None
    recommendation: str = ""
    total_results: int = 0
    credits_used: int = 0

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "region": self.region,
            "currency": self.currency,
            "best_deal": self.best_deal,
            "runner_up": self.runner_up,
            "recommendation": self.recommendation,
            "total_results": self.total_results,
            "all_deals": [d.to_dict() for d in self.deals],
            "credits_used": self.credits_used,
        }


def _get_region_info(region: str) -> tuple[str, str, list[str]]:
    """Return (location_name, currency, list of allowed domains) for a region."""
    reg = _load_registry()
    if region in reg and region != "_global":
        entry = reg[region]
        domains = [r["domain"] for r in entry["retailers"]]
        # Add global retailers
        if "_global" in reg:
            domains += [r["domain"] for r in reg["_global"]["retailers"]]
        return entry["location_name"], entry["currency"], domains
    # Fallback for unknown regions — no domain filtering
    return region, "USD", []


def _domain_to_name(domain: str, region: str) -> str:
    """Look up a friendly retailer name from the registry."""
    reg = _load_registry()
    for section in [region, "_global"]:
        if section in reg:
            retailers = reg[section].get("retailers", [])
            for r in retailers:
                if r["domain"] == domain:
                    return r["name"]
    return domain.split(".")[0].title()


# ---------------------------------------------------------------------------
# Hunt orchestration
# ---------------------------------------------------------------------------

async def hunt(product_query: str, region: str, currency: str, on_event=None) -> HuntResult:
    """
    Run the full 3-tier price hunt.

    on_event: optional async callback(event_type: str, data: dict) for live dashboard updates.
    """
    result = HuntResult(query=product_query, region=region, currency=currency)
    location_name, default_currency, allowed_domains = _get_region_info(region)

    if currency == "" or currency is None:
        currency = default_currency
        result.currency = currency

    if on_event:
        await on_event("hunt_started", {"query": product_query, "region": region})

    # ── Tier 1: Firecrawl Search ──────────────────────────────────────────
    hits = await fc.search_products(product_query, location_name, limit=10)
    result.credits_used += 1

    # Filter by regional domains (if registry exists for this region)
    regional_hits = []
    cross_border_hits = []
    for hit in hits:
        if not allowed_domains:
            # Unknown region — accept everything
            regional_hits.append(hit)
        elif hit.domain in allowed_domains:
            regional_hits.append(hit)
        else:
            cross_border_hits.append(hit)

    # Build deals from snippet prices (FREE — no extra credits)
    for hit in regional_hits:
        if hit.snippet_price is not None:
            deal = DealResult(
                retailer_name=_domain_to_name(hit.domain, region),
                retailer_domain=hit.domain,
                retailer_url=hit.url,
                price=hit.snippet_price,
                currency=hit.snippet_currency or currency,
                final_price=hit.snippet_price,
                tier=1,
            )
            result.deals.append(deal)

    if on_event:
        await on_event("tier1_complete", {
            "results_found": len(hits),
            "regional_matches": len(regional_hits),
            "prices_extracted": len(result.deals),
        })

    # ── Tier 2: Targeted Scrape ───────────────────────────────────────────
    needs_scrape = [h for h in regional_hits if h.needs_scrape][:5]  # cap at 5

    if needs_scrape:
        scrape_tasks = [fc.scrape_product_page(h.url) for h in needs_scrape]
        scraped = await asyncio.gather(*scrape_tasks, return_exceptions=True)
        result.credits_used += len(needs_scrape)

        for hit, scrape_result in zip(needs_scrape, scraped):
            if isinstance(scrape_result, Exception) or scrape_result is None:
                continue

            if on_event:
                await on_event("tier2_result", {
                    "retailer": _domain_to_name(hit.domain, region),
                    "price": scrape_result.price,
                    "currency": scrape_result.currency,
                })

            deal = DealResult(
                retailer_name=_domain_to_name(hit.domain, region),
                retailer_domain=hit.domain,
                retailer_url=hit.url,
                price=scrape_result.price,
                currency=scrape_result.currency,
                final_price=scrape_result.price - (scrape_result.shipping_cost or 0) if scrape_result.shipping_cost and scrape_result.shipping_cost < 0 else scrape_result.price + (scrape_result.shipping_cost or 0),
                original_price=scrape_result.original_price,
                shipping_cost=scrape_result.shipping_cost,
                in_stock=scrape_result.in_stock,
                tier=2,
            )
            result.deals.append(deal)

    # ── Deduplicate by domain (keep lowest price) ─────────────────────────
    seen: dict[str, DealResult] = {}
    for deal in result.deals:
        existing = seen.get(deal.retailer_domain)
        if existing is None or deal.final_price < existing.final_price:
            seen[deal.retailer_domain] = deal
    result.deals = sorted(seen.values(), key=lambda d: d.final_price)
    result.total_results = len(result.deals)

    # ── Gemini analysis ───────────────────────────────────────────────────
    if result.deals:
        deal_dicts = [d.to_dict() for d in result.deals]
        analysis = await gem.analyze_prices(deal_dicts, product_query, region, currency)
        result.recommendation = analysis.get("recommendation", "")

        best_idx = analysis.get("best_deal_index", 0)
        if 0 <= best_idx < len(result.deals):
            result.best_deal = result.deals[best_idx].to_dict()
        else:
            result.best_deal = result.deals[0].to_dict()

        if len(result.deals) > 1:
            runner_idx = 1 if best_idx == 0 else 0
            result.runner_up = result.deals[runner_idx].to_dict()
    else:
        result.recommendation = f"I couldn't find pricing for '{product_query}' in your region. Try a more specific product name."

    if on_event:
        await on_event("hunt_complete", result.to_dict())

    return result
