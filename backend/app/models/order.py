"""
Order models:
  - Order
  - OrderItem
  - PaymentTransaction
"""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger, DateTime, Enum,
    ForeignKey, Integer, Numeric, String, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ── Enums ──────────────────────────────────────────────────────────────────────

class OrderStatusEnum(str, enum.Enum):
    pending    = "pending"
    confirmed  = "confirmed"
    processing = "processing"
    shipped    = "shipped"
    delivered  = "delivered"
    cancelled  = "cancelled"
    refunded   = "refunded"


class PaymentStatusEnum(str, enum.Enum):
    pending  = "pending"
    paid     = "paid"
    failed   = "failed"
    refunded = "refunded"


class TransactionStatusEnum(str, enum.Enum):
    pending   = "pending"
    completed = "completed"
    failed    = "failed"
    refunded  = "refunded"


# ── Models ─────────────────────────────────────────────────────────────────────

class Order(Base):
    __tablename__ = "orders"

    order_id:      Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), index=True
    )
    order_number:  Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    order_status:  Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum), default=OrderStatusEnum.pending, index=True
    )
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending
    )
    subtotal:       Mapped[float | None] = mapped_column(Numeric(12, 2))
    total_amount:   Mapped[float | None] = mapped_column(Numeric(12, 2))
    payment_method: Mapped[str | None]   = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────────────────────
    user:         Mapped["User | None"] = relationship("User", back_populates="orders")
    items:        Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["PaymentTransaction"]] = relationship(
        "PaymentTransaction", back_populates="order", cascade="all, delete-orphan"
    )
    reviews:      Mapped[list["Review"]] = relationship("Review", back_populates="order")
    returns:      Mapped[list["Return"]] = relationship("Return", back_populates="order")

    def __repr__(self) -> str:
        return f"<Order id={self.order_id} number={self.order_number!r} status={self.order_status}>"


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="SET NULL"), index=True
    )
    variant_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("product_variants.variant_id", ondelete="SET NULL")
    )
    quantity:   Mapped[int | None]   = mapped_column(Integer)
    unit_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    subtotal:   Mapped[float | None] = mapped_column(Numeric(12, 2))

    # ── Relationships ────────────────────────────────────────────────────────
    order:   Mapped["Order"]                 = relationship("Order", back_populates="items")
    product: Mapped["Product | None"]        = relationship("Product", back_populates="order_items")
    variant: Mapped["ProductVariant | None"] = relationship(
        "ProductVariant", back_populates="order_items"
    )
    return_items: Mapped[list["ReturnItem"]] = relationship(
        "ReturnItem", back_populates="order_item"
    )

    def __repr__(self) -> str:
        return f"<OrderItem id={self.order_item_id} order_id={self.order_id}>"


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    transaction_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id", ondelete="CASCADE"), index=True
    )
    payment_method:       Mapped[str | None] = mapped_column(String(50))
    transaction_reference:Mapped[str | None] = mapped_column(String(100))
    amount:               Mapped[float | None] = mapped_column(Numeric(12, 2))
    status: Mapped[TransactionStatusEnum] = mapped_column(
        Enum(TransactionStatusEnum), default=TransactionStatusEnum.pending
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    order: Mapped["Order"] = relationship("Order", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<PaymentTransaction id={self.transaction_id} status={self.status}>"


# ── Lazy imports ────────────────────────────────────────────────────────────────
from app.models.user    import User             # noqa: E402
from app.models.product import Product, ProductVariant  # noqa: E402
from app.models.review  import Review           # noqa: E402
from app.models.returns import Return, ReturnItem # noqa: E402
