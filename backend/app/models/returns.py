"""
Return models:
  - Return
  - ReturnItem
"""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger, DateTime, Enum,
    ForeignKey, Integer, Numeric, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReturnStatusEnum(str, enum.Enum):
    requested = "requested"
    approved  = "approved"
    rejected  = "rejected"
    received  = "received"
    refunded  = "refunded"


class Return(Base):
    __tablename__ = "returns"

    return_id:     Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("orders.order_id", ondelete="SET NULL"), index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), index=True
    )
    return_status: Mapped[ReturnStatusEnum] = mapped_column(
        Enum(ReturnStatusEnum), default=ReturnStatusEnum.requested
    )
    refund_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    created_at:    Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    order: Mapped["Order | None"] = relationship("Order", back_populates="returns")
    user:  Mapped["User | None"]  = relationship("User",  back_populates="returns")
    items: Mapped[list["ReturnItem"]] = relationship(
        "ReturnItem", back_populates="return_obj", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Return id={self.return_id} status={self.return_status}>"


class ReturnItem(Base):
    __tablename__ = "return_items"

    return_item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("returns.return_id", ondelete="CASCADE"), index=True
    )
    order_item_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("order_items.order_item_id", ondelete="SET NULL")
    )
    quantity:      Mapped[int | None]   = mapped_column(Integer)
    refund_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))

    # ── Relationships ────────────────────────────────────────────────────────
    return_obj: Mapped["Return"]          = relationship("Return",    back_populates="items")
    order_item: Mapped["OrderItem | None"] = relationship("OrderItem", back_populates="return_items")

    def __repr__(self) -> str:
        return f"<ReturnItem id={self.return_item_id}>"


# ── Lazy imports ────────────────────────────────────────────────────────────────
from app.models.user  import User       # noqa: E402
from app.models.order import Order, OrderItem  # noqa: E402
