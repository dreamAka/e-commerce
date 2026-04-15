"""
Inventory models:
  - Warehouse
  - Inventory
  - InventoryMovement
"""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum,
    ForeignKey, Integer, String, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MovementTypeEnum(str, enum.Enum):
    in_        = "in"
    out        = "out"
    adjustment = "adjustment"
    return_    = "return"
    damage     = "damage"


class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    warehouse_name: Mapped[str | None] = mapped_column(String(100))
    address:        Mapped[str | None] = mapped_column(Text)
    city:           Mapped[str | None] = mapped_column(String(50))
    region:         Mapped[str | None] = mapped_column(String(50))
    phone:          Mapped[str | None] = mapped_column(String(20))
    is_active:      Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:     Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    inventory:       Mapped[list["Inventory"]] = relationship("Inventory", back_populates="warehouse")
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        "PurchaseOrder", back_populates="warehouse"
    )

    def __repr__(self) -> str:
        return f"<Warehouse id={self.warehouse_id} name={self.warehouse_name!r}>"


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id:      Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    variant_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("product_variants.variant_id", ondelete="CASCADE")
    )
    warehouse_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("warehouses.warehouse_id", ondelete="CASCADE"), index=True
    )
    quantity_available: Mapped[int | None] = mapped_column(Integer, default=0)
    quantity_reserved:  Mapped[int | None] = mapped_column(Integer, default=0)
    quantity_damaged:   Mapped[int | None] = mapped_column(Integer, default=0)
    last_restock_date:  Mapped[datetime | None] = mapped_column(DateTime)

    # ── Relationships ────────────────────────────────────────────────────────
    product:   Mapped["Product | None"]        = relationship("Product",        back_populates="inventory")
    variant:   Mapped["ProductVariant | None"] = relationship("ProductVariant", back_populates="inventory")
    warehouse: Mapped["Warehouse | None"]      = relationship("Warehouse",      back_populates="inventory")
    movements: Mapped[list["InventoryMovement"]] = relationship(
        "InventoryMovement", back_populates="inventory", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Inventory id={self.inventory_id} qty={self.quantity_available}>"


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    movement_id:    Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    inventory_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("inventory.inventory_id", ondelete="CASCADE"), index=True
    )
    movement_type:  Mapped[MovementTypeEnum | None] = mapped_column(Enum(MovementTypeEnum))
    quantity:       Mapped[int | None] = mapped_column(Integer)
    reference_type: Mapped[str | None] = mapped_column(String(50))
    reference_id:   Mapped[int | None] = mapped_column(Integer)
    created_by: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    inventory: Mapped["Inventory"]  = relationship("Inventory", back_populates="movements")
    creator:   Mapped["User | None"] = relationship("User")

    def __repr__(self) -> str:
        return f"<InventoryMovement id={self.movement_id} type={self.movement_type}>"


# ── Lazy imports ────────────────────────────────────────────────────────────────
from app.models.product import Product, ProductVariant  # noqa: E402
from app.models.supply  import PurchaseOrder             # noqa: E402
from app.models.user    import User                      # noqa: E402
