"""
Supply-chain models:
  - Supplier
  - PurchaseOrder
  - PurchaseOrderItem
"""

import enum
from datetime import date, datetime

from sqlalchemy import (
    BigInteger, Boolean, Date, DateTime, Enum,
    ForeignKey, Integer, Numeric, String, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PurchaseOrderStatusEnum(str, enum.Enum):
    draft     = "draft"
    sent      = "sent"
    confirmed = "confirmed"
    received  = "received"
    cancelled = "cancelled"


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id:    Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    supplier_name:  Mapped[str | None] = mapped_column(String(100))
    contact_person: Mapped[str | None] = mapped_column(String(100))
    email:          Mapped[str | None] = mapped_column(String(100))
    phone:          Mapped[str | None] = mapped_column(String(20))
    address:        Mapped[str | None] = mapped_column(Text)
    rating:         Mapped[float | None] = mapped_column(Numeric(3, 2))
    is_active:      Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:     Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        "PurchaseOrder", back_populates="supplier"
    )

    def __repr__(self) -> str:
        return f"<Supplier id={self.supplier_id} name={self.supplier_name!r}>"


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    po_id:                  Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    po_number:              Mapped[str | None] = mapped_column(String(50), unique=True)
    supplier_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("suppliers.supplier_id", ondelete="SET NULL"), index=True
    )
    warehouse_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("warehouses.warehouse_id", ondelete="SET NULL"), index=True
    )
    order_date:             Mapped[date | None] = mapped_column(Date)
    expected_delivery_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[PurchaseOrderStatusEnum] = mapped_column(
        Enum(PurchaseOrderStatusEnum), default=PurchaseOrderStatusEnum.draft
    )
    total_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    created_by: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    supplier:  Mapped["Supplier | None"]   = relationship("Supplier",  back_populates="purchase_orders")
    warehouse: Mapped["Warehouse | None"]  = relationship("Warehouse", back_populates="purchase_orders")
    creator:   Mapped["User | None"]       = relationship("User")
    items:     Mapped[list["PurchaseOrderItem"]] = relationship(
        "PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<PurchaseOrder po_id={self.po_id} number={self.po_number!r}>"


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    po_item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    po_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("purchase_orders.po_id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="SET NULL")
    )
    variant_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("product_variants.variant_id", ondelete="SET NULL")
    )
    quantity_ordered:  Mapped[int | None]   = mapped_column(Integer)
    quantity_received: Mapped[int | None]   = mapped_column(Integer, default=0)
    unit_price:        Mapped[float | None] = mapped_column(Numeric(12, 2))

    # ── Relationships ────────────────────────────────────────────────────────
    purchase_order: Mapped["PurchaseOrder"]         = relationship("PurchaseOrder", back_populates="items")
    product:        Mapped["Product | None"]        = relationship("Product",        back_populates="purchase_order_items")
    variant:        Mapped["ProductVariant | None"] = relationship("ProductVariant", back_populates="purchase_order_items")

    def __repr__(self) -> str:
        return f"<PurchaseOrderItem po_item_id={self.po_item_id}>"


# ── Lazy imports ────────────────────────────────────────────────────────────────
from app.models.inventory import Warehouse              # noqa: E402
from app.models.product   import Product, ProductVariant # noqa: E402
from app.models.user      import User                    # noqa: E402
