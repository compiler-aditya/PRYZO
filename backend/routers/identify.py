"""Visual Product Identification — camera → Gemini vision → product name."""

from pydantic import BaseModel
from fastapi import APIRouter, Depends

from config import BACKEND_SECRET
from services.gemini_service import identify_product

router = APIRouter()


class IdentifyRequest(BaseModel):
    image_b64: str  # base64-encoded image from camera
    mime_type: str = "image/jpeg"


class IdentifyResponse(BaseModel):
    identified: bool
    confidence: str = "low"
    brand: str = ""
    model: str = ""
    product_name: str = ""
    category: str = ""
    color: str = ""
    variants: list[str] = []
    search_query: str = ""
    ambiguity_note: str = ""


@router.post("/api/identify", response_model=IdentifyResponse)
async def identify(req: IdentifyRequest):
    """Identify a product from a camera image. Returns product info for hunt."""
    result = await identify_product(req.image_b64, req.mime_type)
    return IdentifyResponse(
        identified=result.get("identified", False),
        confidence=result.get("confidence", "low"),
        brand=result.get("brand", ""),
        model=result.get("model", ""),
        product_name=result.get("product_name", ""),
        category=result.get("category", ""),
        color=result.get("color", ""),
        variants=result.get("variants", []),
        search_query=result.get("search_query", ""),
        ambiguity_note=result.get("ambiguity_note", ""),
    )
