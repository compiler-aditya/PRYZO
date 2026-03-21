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
# Data classes
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
    # Verification fields
    trust_score: int = 50  # 0-100, higher = more trustworthy
    condition: str = "unknown"  # new, refurbished, open_box, unknown
    warnings: list[str] = field(default_factory=list)
    verified_price: float | None = None  # Gemini's opinion of the real price
    seller_type: str = "unknown"  # official, trusted_third_party, unknown_seller

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
            "trust_score": self.trust_score,
            "condition": self.condition,
            "warnings": self.warnings,
            "verified_price": self.verified_price,
            "seller_type": self.seller_type,
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
    cross_border_option: dict | None = None

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
            "cross_border_option": self.cross_border_option,
        }


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------

def _get_region_info(region: str) -> tuple[str, str, list[str]]:
    """Return (location_name, currency, list of allowed base domains) for a region."""
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


def _domain_matches_registry(domain: str, allowed_domains: list[str]) -> bool:
    """Check if domain or its base domain matches allowed list.

    Handles subdomains: luxury.tatacliq.com matches tatacliq.com.
    """
    if domain in allowed_domains:
        return True
    base = fc.extract_base_domain(domain)
    if base in allowed_domains:
        return True
    # Check if any allowed domain is a suffix of this domain
    for allowed in allowed_domains:
        if domain.endswith("." + allowed):
            return True
    return False


def _domain_to_name(domain: str, region: str) -> str:
    """Look up a friendly retailer name from the registry."""
    reg = _load_registry()
    base = fc.extract_base_domain(domain)
    for section in [region, "_global"]:
        if section in reg:
            retailers = reg[section].get("retailers", [])
            for r in retailers:
                if r["domain"] == domain or r["domain"] == base:
                    return r["name"]
    return domain.split(".")[0].title()


def _get_expected_currency(region: str) -> str | None:
    """Return the expected currency for a region, or None if unknown."""
    reg = _load_registry()
    if region in reg and region != "_global":
        return reg[region].get("currency")
    return None


# ---------------------------------------------------------------------------
# Price validation helpers
# ---------------------------------------------------------------------------

def _compute_final_price(price: float, shipping: float | None) -> float:
    """Compute final price = price + shipping (if shipping is positive)."""
    if shipping and shipping > 0:
        return price + shipping
    return price


def _filter_outliers(deals: list[DealResult]) -> list[DealResult]:
    """Remove statistically implausible prices using IQR method.

    Catches both suspiciously low (snippet artifacts like ₹349 for headphones)
    and suspiciously high prices (inflated marketplace listings).
    """
    if len(deals) < 3:
        return deals

    prices = sorted(d.final_price for d in deals)
    n = len(prices)
    q1 = prices[n // 4]
    q3 = prices[(3 * n) // 4]
    iqr = q3 - q1

    if iqr == 0:
        # All prices are similar — use median-based filter instead
        median = prices[n // 2]
        lower = median * 0.15
        upper = median * 3.0
    else:
        lower = q1 - 2.0 * iqr
        upper = q3 + 2.0 * iqr

    # Absolute floor: no product costs less than ₹100/$1
    lower = max(lower, 50)

    filtered = [d for d in deals if lower <= d.final_price <= upper]

    # Never filter everything — keep at least the median-priced deals
    if not filtered:
        median = prices[n // 2]
        filtered = [d for d in deals if d.final_price == median]

    removed = len(deals) - len(filtered)
    if removed:
        log.info("Outlier filter removed %d of %d deals (range: %.0f–%.0f)", removed, len(deals), lower, upper)

    return filtered


def _has_currency_mismatch(deal: DealResult, expected_currency: str | None) -> bool:
    """Detect if a deal's currency doesn't match the expected region currency.

    e.g., a USD price from amazon.in is wrong.
    """
    if not expected_currency:
        return False
    return deal.currency != expected_currency


# ---------------------------------------------------------------------------
# Hunt orchestration
# ---------------------------------------------------------------------------

SCRAPE_TIMEOUT = 20  # seconds per scrape task


async def _scrape_with_timeout(url: str, timeout: int = SCRAPE_TIMEOUT):
    """Wrap scrape in asyncio timeout so one slow page doesn't block the hunt."""
    try:
        return await asyncio.wait_for(fc.scrape_product_page(url), timeout=timeout)
    except asyncio.TimeoutError:
        log.warning("Scrape timed out for %s", url)
        return None


async def hunt(product_query: str, region: str, currency: str, on_event=None) -> HuntResult:
    """
    Run the full 3-tier price hunt.

    on_event: optional async callback(event_type: str, data: dict) for live dashboard updates.
    """
    result = HuntResult(query=product_query, region=region, currency=currency)
    location_name, default_currency, allowed_domains = _get_region_info(region)
    expected_currency = _get_expected_currency(region)

    if not currency:
        currency = default_currency
        result.currency = currency

    if on_event:
        await on_event("hunt_started", {"query": product_query, "region": region})

    # ── Tier 1: Firecrawl Search ──────────────────────────────────────────
    hits = await fc.search_products(product_query, location_name, limit=10)
    result.credits_used += 1

    # If zero results, retry with a simpler query (drop "price buy online in")
    if not hits:
        log.info("No results with regional query, retrying with broader search")
        hits = await fc.search_products(product_query, location_name, limit=10)
        result.credits_used += 1

    # Classify hits as regional or cross-border
    regional_hits: list[fc.SearchHit] = []
    cross_border_hits: list[fc.SearchHit] = []

    for hit in hits:
        if not allowed_domains:
            # Unknown region — accept everything
            regional_hits.append(hit)
        elif _domain_matches_registry(hit.domain, allowed_domains):
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
    # Scrape: (a) regional hits without a snippet price, (b) top regional hits
    # even if they have a snippet price (scraped is more accurate), cap at 5
    needs_scrape = [h for h in regional_hits if h.needs_scrape]

    # Also re-scrape top 2 snippet-priced hits for accuracy (Tier 2 > Tier 1)
    with_price = [h for h in regional_hits if not h.needs_scrape]
    rescrape = with_price[:2]
    all_to_scrape = needs_scrape + rescrape
    # Deduplicate by URL
    seen_urls: set[str] = set()
    unique_scrape: list[fc.SearchHit] = []
    for h in all_to_scrape:
        if h.url not in seen_urls:
            seen_urls.add(h.url)
            unique_scrape.append(h)
    unique_scrape = unique_scrape[:5]  # cap at 5

    # Track page markdown per deal for verification
    deal_markdown: dict[str, str] = {}  # domain → page markdown

    if unique_scrape:
        scrape_tasks = [_scrape_with_timeout(h.url) for h in unique_scrape]
        scraped = await asyncio.gather(*scrape_tasks, return_exceptions=True)
        result.credits_used += len(unique_scrape)

        for hit, scrape_result in zip(unique_scrape, scraped):
            if isinstance(scrape_result, Exception) or scrape_result is None:
                log.debug("Scrape failed/empty for %s", hit.url)
                continue

            final = _compute_final_price(scrape_result.price, scrape_result.shipping_cost)

            if on_event:
                await on_event("tier2_result", {
                    "retailer": _domain_to_name(hit.domain, region),
                    "price": scrape_result.price,
                    "currency": scrape_result.currency,
                    "in_stock": scrape_result.in_stock,
                })

            deal = DealResult(
                retailer_name=_domain_to_name(hit.domain, region),
                retailer_domain=hit.domain,
                retailer_url=hit.url,
                price=scrape_result.price,
                currency=scrape_result.currency,
                final_price=final,
                original_price=scrape_result.original_price,
                shipping_cost=scrape_result.shipping_cost if scrape_result.shipping_cost and scrape_result.shipping_cost > 0 else None,
                in_stock=scrape_result.in_stock,
                tier=2,
            )
            result.deals.append(deal)

            # Store markdown for verification
            if scrape_result.page_markdown:
                deal_markdown[hit.domain] = scrape_result.page_markdown

    # ── Deduplicate by base domain ──────────────────────────────────────
    # Prefer Tier 2 (scraped) over Tier 1 (snippet) for the same domain,
    # since scraped prices are more accurate.
    seen: dict[str, DealResult] = {}
    for deal in result.deals:
        base = fc.extract_base_domain(deal.retailer_domain)
        existing = seen.get(base)
        if existing is None:
            seen[base] = deal
        elif deal.tier > existing.tier:
            # Higher tier = more accurate (Tier 2 beats Tier 1)
            seen[base] = deal
        elif deal.tier == existing.tier and deal.final_price < existing.final_price:
            seen[base] = deal
    deduped = list(seen.values())

    # ── Currency mismatch detection ──────────────────────────────────────
    # Remove deals with wrong currency (e.g., USD from amazon.in)
    if expected_currency:
        valid = []
        for d in deduped:
            if _has_currency_mismatch(d, expected_currency):
                log.info("Currency mismatch: %s has %s, expected %s — dropping", d.retailer_domain, d.currency, expected_currency)
            else:
                valid.append(d)
        # Only apply if we'd still have results
        if valid:
            deduped = valid

    # ── Filter outlier prices ────────────────────────────────────────────
    deduped = _filter_outliers(deduped)

    # ── Gemini Deal Verification (FREE — no Firecrawl credits) ──────────
    # Verify each Tier 2 deal that has page markdown.
    # Catches: variant bait, conditional pricing, refurbished, hidden fees.
    deals_to_verify = [d for d in deduped if d.tier == 2 and deal_markdown.get(d.retailer_domain)]

    if deals_to_verify:
        if on_event:
            await on_event("verification_started", {"count": len(deals_to_verify)})

        verify_tasks = [
            gem.verify_deal(
                product_query=product_query,
                scraped_price=d.price,
                scraped_currency=d.currency,
                original_price=d.original_price,
                page_markdown=deal_markdown[d.retailer_domain],
            )
            for d in deals_to_verify
        ]
        verifications = await asyncio.gather(*verify_tasks, return_exceptions=True)

        for deal, vresult in zip(deals_to_verify, verifications):
            if isinstance(vresult, Exception):
                log.warning("Verification failed for %s: %s", deal.retailer_domain, vresult)
                continue

            deal.trust_score = vresult.get("trust_score", 50)
            deal.condition = vresult.get("condition", "unknown")
            deal.warnings = vresult.get("warnings", [])
            deal.seller_type = vresult.get("seller_type", "unknown")

            # If Gemini found a different actual price, record it
            verified_price = vresult.get("verified_price")
            if verified_price and isinstance(verified_price, (int, float)) and verified_price != deal.price:
                deal.verified_price = float(verified_price)
                # Use verified price as final_price if it's higher (deceptive low price)
                if deal.verified_price > deal.final_price:
                    log.info(
                        "Price adjusted for %s: scraped=%.0f, verified=%.0f (%s)",
                        deal.retailer_domain, deal.final_price, deal.verified_price,
                        vresult.get("adjusted_reason", ""),
                    )
                    deal.final_price = deal.verified_price

            # Mark refurbished/renewed deals
            if deal.condition in ("refurbished", "open_box"):
                deal.warnings.append(f"This is a {deal.condition} unit, not brand new")

            if on_event:
                await on_event("deal_verified", {
                    "retailer": deal.retailer_name,
                    "trust_score": deal.trust_score,
                    "warnings": deal.warnings,
                })

    # ── Sort: in-stock first, then by trust (high=better), then by price ─
    deduped.sort(key=lambda d: (
        not d.in_stock,          # in-stock first
        d.condition != "new",    # new condition first
        -(d.trust_score or 50),  # higher trust first (negative for ascending sort)
        d.final_price,           # lower price first
    ))

    result.deals = deduped
    result.total_results = len(result.deals)

    # ── Cross-border deal evaluation ─────────────────────────────────────
    # If there are cross-border hits with prices, check if any beats domestic
    if cross_border_hits and result.deals:
        best_domestic = result.deals[0].final_price if result.deals[0].in_stock else None
        best_cb: fc.SearchHit | None = None
        for cbh in cross_border_hits:
            if cbh.snippet_price is not None:
                if best_cb is None or cbh.snippet_price < best_cb.snippet_price:
                    best_cb = cbh

        if best_cb and best_cb.snippet_price and best_domestic:
            # Only evaluate if cross-border is >20% cheaper (to justify import duty)
            if best_cb.snippet_price < best_domestic * 0.8:
                try:
                    cb_estimate = await gem.estimate_cross_border_cost(
                        best_cb.snippet_price,
                        best_cb.snippet_currency or "USD",
                        currency,
                    )
                    total_high = cb_estimate.get("total_estimate_high", best_cb.snippet_price)
                    if total_high < best_domestic:
                        result.cross_border_option = {
                            "retailer": best_cb.domain,
                            "url": best_cb.url,
                            "foreign_price": best_cb.snippet_price,
                            "foreign_currency": best_cb.snippet_currency,
                            **cb_estimate,
                        }
                except Exception as e:
                    log.warning("Cross-border estimation failed: %s", e)

    # ── Gemini analysis ───────────────────────────────────────────────────
    if result.deals:
        # Separate in-stock and out-of-stock for analysis
        in_stock_deals = [d for d in result.deals if d.in_stock]
        deal_dicts = [d.to_dict() for d in result.deals]

        analysis = await gem.analyze_prices(deal_dicts, product_query, region, currency)
        result.recommendation = analysis.get("recommendation", "")

        best_idx = analysis.get("best_deal_index", 0)
        if 0 <= best_idx < len(result.deals):
            chosen = result.deals[best_idx]
            # Don't recommend out-of-stock as best deal
            if not chosen.in_stock and in_stock_deals:
                chosen = in_stock_deals[0]
            result.best_deal = chosen.to_dict()
        elif in_stock_deals:
            result.best_deal = in_stock_deals[0].to_dict()
        elif result.deals:
            result.best_deal = result.deals[0].to_dict()

        # Runner up: next best in-stock deal that isn't the best
        best_domain = result.best_deal.get("retailer_domain") if result.best_deal else None
        for d in result.deals:
            if d.in_stock and d.retailer_domain != best_domain:
                result.runner_up = d.to_dict()
                break
        # Fallback: any deal that isn't the best
        if not result.runner_up and len(result.deals) > 1:
            for d in result.deals:
                if d.retailer_domain != best_domain:
                    result.runner_up = d.to_dict()
                    break
    else:
        result.recommendation = (
            f"I couldn't find pricing for '{product_query}' in {location_name}. "
            "Try a more specific product name or check the spelling."
        )

    if on_event:
        await on_event("hunt_complete", result.to_dict())

    return result
