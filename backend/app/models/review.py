"""
Review models:
  - Review
  - ReviewImage
  - ReviewReaction
"""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum,
    ForeignKey, Integer, String, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReactionTypeEnum(str, enum.Enum):
    helpful   = "helpful"
    unhelpful = "unhelpful"


class Review(Base):
    __tablename__ = "reviews"

    review_id:  Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), index=True
    )
    order_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("orders.order_id", ondelete="SET NULL")
    )
    rating:      Mapped[int | None] = mapped_column(Integer)
    comment:     Mapped[str | None] = mapped_column(Text)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:  Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    product:   Mapped["Product | None"] = relationship("Product", back_populates="reviews")
    user:      Mapped["User | None"]    = relationship("User",    back_populates="reviews")
    order:     Mapped["Order | None"]   = relationship("Order",   back_populates="reviews")
    images:    Mapped[list["ReviewImage"]] = relationship(
        "ReviewImage", back_populates="review", cascade="all, delete-orphan"
    )
    reactions: Mapped[list["ReviewReaction"]] = relationship(
        "ReviewReaction", back_populates="review", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Review id={self.review_id} rating={self.rating}>"


class ReviewImage(Base):
    __tablename__ = "review_images"

    review_image_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    review_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("reviews.review_id", ondelete="CASCADE"), index=True
    )
    image_url: Mapped[str | None] = mapped_column(String(255))

    # ── Relationships ────────────────────────────────────────────────────────
    review: Mapped["Review"] = relationship("Review", back_populates="images")


class ReviewReaction(Base):
    __tablename__ = "review_reactions"

    reaction_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    review_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("reviews.review_id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), index=True
    )
    reaction_type: Mapped[ReactionTypeEnum | None] = mapped_column(Enum(ReactionTypeEnum))
    created_at:    Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    review: Mapped["Review"]      = relationship("Review", back_populates="reactions")
    user:   Mapped["User | None"] = relationship("User",   back_populates="review_reactions")


# ── Lazy imports ────────────────────────────────────────────────────────────────
from app.models.product import Product  # noqa: E402
from app.models.user    import User     # noqa: E402
from app.models.order   import Order    # noqa: E402
