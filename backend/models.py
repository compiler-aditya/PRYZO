import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class PriceResult(Base):
    __tablename__ = "price_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String, index=True)
    product_query: Mapped[str] = mapped_column(String)
    retailer_name: Mapped[str] = mapped_column(String)
    retailer_domain: Mapped[str] = mapped_column(String)
    retailer_url: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    original_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    shipping_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    coupon_code: Mapped[str | None] = mapped_column(String, nullable=True)
    coupon_discount: Mapped[float | None] = mapped_column(Float, nullable=True)
    final_price: Mapped[float] = mapped_column(Float)
    region: Mapped[str] = mapped_column(String)
    tier: Mapped[int] = mapped_column(Integer, default=1)
    is_cross_border: Mapped[bool] = mapped_column(Boolean, default=False)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class PriceWatch(Base):
    __tablename__ = "price_watches"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    product_query: Mapped[str] = mapped_column(String)
    target_price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    session_id: Mapped[str | None] = mapped_column(String, nullable=True)
    current_best_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    best_retailer_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")  # active, triggered, expired, cancelled
    check_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
