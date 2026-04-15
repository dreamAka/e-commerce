"""
Shopping cart model
"""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    cart_id:    Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    variant_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("product_variants.variant_id", ondelete="SET NULL")
    )
    quantity: Mapped[int | None] = mapped_column(Integer, default=1)
    added_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    user:    Mapped["User | None"]           = relationship("User",           back_populates="cart_items")
    product: Mapped["Product | None"]        = relationship("Product",        back_populates="cart_items")
    variant: Mapped["ProductVariant | None"] = relationship("ProductVariant", back_populates="cart_items")

    def __repr__(self) -> str:
        return f"<ShoppingCart id={self.cart_id} user_id={self.user_id}>"


# ── Lazy imports ────────────────────────────────────────────────────────────────
from app.models.user    import User                     # noqa: E402
from app.models.product import Product, ProductVariant  # noqa: E402
