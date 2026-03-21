"""Hunt Mode API — called by ElevenAgents server tool."""

import logging
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from config import BACKEND_SECRET
from database import get_db
from models import PriceResult
from services.price_engine import hunt, HuntResult

log = logging.getLogger(__name__)
router = APIRouter()

# WebSocket connections for live dashboard (session_id → list of WS)
_ws_connections: dict[str, list] = {}


def register_ws(session_id: str, ws):
    _ws_connections.setdefault(session_id, []).append(ws)


def unregister_ws(session_id: str, ws):
    conns = _ws_connections.get(session_id, [])
    if ws in conns:
        conns.remove(ws)


class HuntRequest(BaseModel):
    product_query: str
    region: str = "US"
    currency: str = ""
    session_id: str = ""


class HuntResponse(BaseModel):
    query: str
    region: str
    currency: str
    best_deal: dict | None = None
    runner_up: dict | None = None
    recommendation: str = ""
    total_results: int = 0
    all_deals: list[dict] = []
    credits_used: int = 0
    cross_border_option: dict | None = None


def _verify_secret(authorization: str = Header(default="")):
    """Simple bearer token check for server tool auth."""
    if not BACKEND_SECRET or BACKEND_SECRET == "dev-secret":
        return  # skip in dev
    token = authorization.replace("Bearer ", "").strip()
    if token != BACKEND_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/api/hunt", response_model=HuntResponse)
async def hunt_product(req: HuntRequest, db: Session = Depends(get_db), _=Depends(_verify_secret)):
    """Run the 3-tier price hunt. Called by ElevenAgents server tool."""
    import json

    async def on_event(event_type: str, data: dict):
        """Push live updates to connected dashboard WebSockets."""
        conns = _ws_connections.get(req.session_id, [])
        msg = json.dumps({"event": event_type, **data})
        for ws in conns:
            try:
                await ws.send_text(msg)
            except Exception:
                pass

    result: HuntResult = await hunt(
        product_query=req.product_query,
        region=req.region,
        currency=req.currency,
        on_event=on_event if req.session_id else None,
    )

    # Persist results to DB
    for deal in result.deals:
        row = PriceResult(
            session_id=req.session_id or "anonymous",
            product_query=req.product_query,
            retailer_name=deal.retailer_name,
            retailer_domain=deal.retailer_domain,
            retailer_url=deal.retailer_url,
            price=deal.price,
            currency=deal.currency,
            original_price=deal.original_price,
            shipping_cost=deal.shipping_cost,
            in_stock=deal.in_stock,
            coupon_code=deal.coupon_code,
            coupon_discount=deal.coupon_discount,
            final_price=deal.final_price,
            region=req.region,
            tier=deal.tier,
            is_cross_border=deal.is_cross_border,
        )
        db.add(row)
    db.commit()

    return result.to_dict()
