"""ElevenLabs Agent integration — signed URL, webhooks, compare, watch, sounds."""

import logging
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from config import HUNT_AGENT_ID
from database import get_db
from models import PriceWatch
from services import elevenlabs_service as el
from services.price_engine import hunt

log = logging.getLogger(__name__)
router = APIRouter()


# ---------------------------------------------------------------------------
# Agent signed URL (for private widget embedding)
# ---------------------------------------------------------------------------

@router.get("/api/agent/signed-url")
async def get_signed_url():
    """Get a signed URL for the ElevenLabs widget. Used by the frontend."""
    if not HUNT_AGENT_ID:
        return {"error": "HUNT_AGENT_ID not configured"}
    url = el.get_signed_url(HUNT_AGENT_ID)
    return {"signed_url": url}


# ---------------------------------------------------------------------------
# Compare endpoint — parallel hunt for two products
# ---------------------------------------------------------------------------

class CompareRequest(BaseModel):
    product_a: str
    product_b: str
    region: str = "US"
    currency: str = ""


@router.post("/api/compare")
async def compare_products(req: CompareRequest):
    """Hunt two products in parallel and return side-by-side comparison.

    Chain: ElevenAgents → compare_products tool → parallel hunt × 2 → Gemini verdict.
    """
    import asyncio
    from services import gemini_service as gem

    # Run both hunts in parallel — same credit cost as two separate hunts
    result_a, result_b = await asyncio.gather(
        hunt(req.product_a, req.region, req.currency),
        hunt(req.product_b, req.region, req.currency),
    )

    # Ask Gemini for a comparative verdict
    comparison_prompt = f"""Compare these two products for a buyer in {req.region}:

Product A: "{req.product_a}"
- Best deal: {result_a.best_deal}
- Total options found: {result_a.total_results}

Product B: "{req.product_b}"
- Best deal: {result_b.best_deal}
- Total options found: {result_b.total_results}

Give a concise comparison (3-4 sentences) covering: price difference, value for money, and which one to buy. Respond as plain text, not JSON."""

    verdict = await gem._ask(comparison_prompt)

    return {
        "product_a": result_a.to_dict(),
        "product_b": result_b.to_dict(),
        "verdict": verdict,
        "total_credits_used": result_a.credits_used + result_b.credits_used,
    }


# ---------------------------------------------------------------------------
# Watch endpoint — create price monitoring
# ---------------------------------------------------------------------------

class WatchRequest(BaseModel):
    product_query: str
    target_price: float
    currency: str = "INR"
    region: str = "IN"
    email: str = ""
    session_id: str = ""


@router.post("/api/watch")
async def create_watch(req: WatchRequest, db: Session = Depends(get_db)):
    """Set up price monitoring. Scheduler (built separately) checks periodically.

    Chain: ElevenAgents → create_watch tool → DB record → Scheduler → Firecrawl Search
    → Price drop detected → ElevenLabs TTS → Audio notification pushed.
    """
    watch = PriceWatch(
        product_query=req.product_query,
        target_price=req.target_price,
        currency=req.currency,
        region=req.region,
        email=req.email,
        session_id=req.session_id or "anonymous",
        status="active",
    )
    db.add(watch)
    db.commit()
    db.refresh(watch)

    return {
        "watch_id": watch.id,
        "product_query": req.product_query,
        "target_price": req.target_price,
        "currency": req.currency,
        "region": req.region,
        "status": "active",
        "message": f"Watching '{req.product_query}' — I'll alert you when it drops below {req.currency} {req.target_price}",
    }


# ---------------------------------------------------------------------------
# Sound effects endpoint — deal quality audio cues
# ---------------------------------------------------------------------------

@router.get("/api/sound/{quality}")
async def get_deal_sound(quality: str):
    """Generate a sound effect for deal quality feedback.

    Chain: Hunt complete → trust_score → client tool play_deal_sound → GET /api/sound/{quality}
    """
    if quality not in ("great", "good", "warning"):
        quality = "good"

    audio = await el.generate_deal_sound(quality)
    if not audio:
        return Response(status_code=204)

    return Response(content=audio, media_type="audio/mpeg")


# ---------------------------------------------------------------------------
# TTS alert generation — for Watch Mode notifications
# ---------------------------------------------------------------------------

class AlertRequest(BaseModel):
    text: str
    voice_id: str = ""


@router.post("/api/alert/tts")
async def generate_alert(req: AlertRequest):
    """Generate a voice alert MP3 for push notifications.

    Chain: Scheduler detects price drop → formats message → POST /api/alert/tts
    → Returns MP3 audio → pushed to user's browser as notification with audio.
    """
    audio = await el.generate_voice_alert(req.text, req.voice_id or el.ALERT_VOICE_ID)
    if not audio:
        return Response(status_code=500)

    return Response(content=audio, media_type="audio/mpeg")


# ---------------------------------------------------------------------------
# Webhook — post-call transcription from ElevenLabs
# ---------------------------------------------------------------------------

@router.post("/api/webhook/elevenlabs")
async def elevenlabs_webhook(request_data: dict):
    """Receive post-call webhooks from ElevenLabs for analytics.

    Logs conversation transcripts and tool usage for debugging.
    """
    event_type = request_data.get("type", "unknown")
    log.info("ElevenLabs webhook: %s", event_type)

    if event_type == "post_call_transcription":
        conversation_id = request_data.get("data", {}).get("conversation_id", "")
        log.info("Call completed: %s", conversation_id)

    return {"status": "received"}
