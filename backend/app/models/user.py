"""
User-related models:
  - User
  - Address
  - UserSession
  - PasswordResetToken
  - EmailVerificationToken
"""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, Date, DateTime, Enum,
    ForeignKey, Integer, Numeric, String, Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ── Enums ──────────────────────────────────────────────────────────────────────

class GenderEnum(str, enum.Enum):
    male   = "male"
    female = "female"
    other  = "other"


class AccountStatusEnum(str, enum.Enum):
    active    = "active"
    inactive  = "inactive"
    suspended = "suspended"
    deleted   = "deleted"


class UserTypeEnum(str, enum.Enum):
    customer = "customer"
    seller   = "seller"
    admin    = "admin"


class AddressTypeEnum(str, enum.Enum):
    shipping = "shipping"
    billing  = "billing"
    both     = "both"


# ── Models ─────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name:  Mapped[str | None] = mapped_column(String(50))
    phone:      Mapped[str | None] = mapped_column(String(20))
    date_of_birth: Mapped[datetime | None] = mapped_column(Date)
    gender:     Mapped[GenderEnum | None] = mapped_column(Enum(GenderEnum))
    profile_image_url: Mapped[str | None] = mapped_column(String(255))

    registration_date: Mapped[datetime | None] = mapped_column(DateTime)
    last_login:        Mapped[datetime | None] = mapped_column(DateTime)

    account_status: Mapped[AccountStatusEnum] = mapped_column(
        Enum(AccountStatusEnum), default=AccountStatusEnum.active
    )
    user_type: Mapped[UserTypeEnum] = mapped_column(
        Enum(UserTypeEnum), default=UserTypeEnum.customer
    )

    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    phone_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    customer_segment:  Mapped[str | None]   = mapped_column(String(50))
    lifetime_value:    Mapped[float | None]  = mapped_column(Numeric(12, 2))
    loyalty_points:    Mapped[int | None]    = mapped_column(Integer, default=0)
    preferred_language:Mapped[str | None]    = mapped_column(String(10), default="uz")
    timezone:          Mapped[str | None]    = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────────────────────
    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="user")
    sessions:  Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user")
    orders:    Mapped[list["Order"]] = relationship("Order", back_populates="user")
    reviews:   Mapped[list["Review"]] = relationship("Review", back_populates="user")
    cart_items:Mapped[list["ShoppingCart"]] = relationship("ShoppingCart", back_populates="user")
    products:  Mapped[list["Product"]] = relationship("Product", back_populates="seller")
    password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(
        "PasswordResetToken", back_populates="user"
    )
    email_verification_tokens: Mapped[list["EmailVerificationToken"]] = relationship(
        "EmailVerificationToken", back_populates="user"
    )
    returns: Mapped[list["Return"]] = relationship("Return", back_populates="user")
    review_reactions: Mapped[list["ReviewReaction"]] = relationship(
        "ReviewReaction", back_populates="user"
    )
    questions: Mapped[list["ProductQuestion"]] = relationship(
        "ProductQuestion", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User id={self.user_id} username={self.username!r}>"


class Address(Base):
    __tablename__ = "addresses"

    address_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), index=True
    )
    address_type: Mapped[AddressTypeEnum] = mapped_column(Enum(AddressTypeEnum))
    is_default:   Mapped[bool] = mapped_column(Boolean, default=False)

    full_name:      Mapped[str | None] = mapped_column(String(100))
    phone:          Mapped[str | None] = mapped_column(String(20))
    country:        Mapped[str | None] = mapped_column(String(50))
    region:         Mapped[str | None] = mapped_column(String(50))
    city:           Mapped[str | None] = mapped_column(String(50))
    district:       Mapped[str | None] = mapped_column(String(50))
    street_address: Mapped[str | None] = mapped_column(Text)
    postal_code:    Mapped[str | None] = mapped_column(String(20))
    latitude:       Mapped[float | None] = mapped_column(Numeric(10, 8))
    longitude:      Mapped[float | None] = mapped_column(Numeric(11, 8))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"<Address id={self.address_id} city={self.city!r}>"


class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id:    Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), index=True
    )
    session_token: Mapped[str] = mapped_column(String(255), unique=True)
    ip_address:    Mapped[str | None] = mapped_column(String(45))
    user_agent:    Mapped[str | None] = mapped_column(Text)
    device_type:   Mapped[str | None] = mapped_column(String(20))
    expires_at:    Mapped[datetime | None] = mapped_column(DateTime)
    created_at:    Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_activity: Mapped[datetime | None] = mapped_column(DateTime)

    # ── Relationships ────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<UserSession id={self.session_id} user_id={self.user_id}>"


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    token_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), index=True
    )
    token:      Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    used:       Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="password_reset_tokens")


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    token_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), index=True
    )
    token:      Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    verified:   Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="email_verification_tokens")


# ── Lazy imports to avoid circular refs ────────────────────────────────────────
from app.models.product import Product          # noqa: E402
from app.models.order   import Order            # noqa: E402
from app.models.review  import Review, ReviewReaction  # noqa: E402
from app.models.cart    import ShoppingCart     # noqa: E402
from app.models.returns import Return           # noqa: E402
from app.models.product import ProductQuestion  # noqa: E402
