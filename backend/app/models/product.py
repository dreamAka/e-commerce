"""
Catalog models:
  - Category  (self-referencing tree)
  - Brand
  - Product
  - ProductVariant
  - VariantAttribute
  - ProductImage
  - ProductAttribute
  - ProductAttributeValue
  - Tag / ProductTag
  - ProductQuestion
"""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum,
    ForeignKey, Integer, Numeric, String, Text,
    Table, Column, UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ── Enums ──────────────────────────────────────────────────────────────────────

class ProductStatusEnum(str, enum.Enum):
    draft         = "draft"
    active        = "active"
    out_of_stock  = "out_of_stock"
    discontinued  = "discontinued"


class AttributeTypeEnum(str, enum.Enum):
    text        = "text"
    number      = "number"
    boolean     = "boolean"
    select      = "select"
    multiselect = "multiselect"


# ── Many-to-Many helper table (product_tags) ────────────────────────────────────
product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"),
           primary_key=True),
    Column("tag_id",     BigInteger, ForeignKey("tags.tag_id",     ondelete="CASCADE"),
           primary_key=True),
)


# ── Models ─────────────────────────────────────────────────────────────────────

class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parent_category_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categories.category_id", ondelete="SET NULL")
    )
    category_name: Mapped[str | None] = mapped_column(String(100))
    description:   Mapped[str | None] = mapped_column(Text)
    slug:          Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    image_url:     Mapped[str | None] = mapped_column(String(255))
    is_active:     Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:    Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at:    Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # ── Self-referencing relationship ────────────────────────────────────────
    parent:   Mapped["Category | None"] = relationship(
        "Category", back_populates="children", remote_side="Category.category_id"
    )
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")

    products:          Mapped[list["Product"]] = relationship("Product", back_populates="category")
    product_attributes:Mapped[list["ProductAttribute"]] = relationship(
        "ProductAttribute", back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.category_id} name={self.category_name!r}>"


class Brand(Base):
    __tablename__ = "brands"

    brand_id:          Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    brand_name:        Mapped[str | None] = mapped_column(String(100))
    description:       Mapped[str | None] = mapped_column(Text)
    logo_url:          Mapped[str | None] = mapped_column(String(255))
    website_url:       Mapped[str | None] = mapped_column(String(255))
    country_of_origin: Mapped[str | None] = mapped_column(String(50))
    is_active:         Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:        Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at:        Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")

    def __repr__(self) -> str:
        return f"<Brand id={self.brand_id} name={self.brand_name!r}>"


class Product(Base):
    __tablename__ = "products"

    product_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    seller_id:    Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), index=True
    )
    category_id:  Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("categories.category_id", ondelete="SET NULL"), index=True
    )
    brand_id:     Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("brands.brand_id", ondelete="SET NULL"), index=True
    )

    product_name:   Mapped[str | None] = mapped_column(String(255))
    slug:           Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    sku:            Mapped[str | None] = mapped_column(String(100), unique=True)
    barcode:        Mapped[str | None] = mapped_column(String(100))
    description:    Mapped[str | None] = mapped_column(Text)

    base_price:     Mapped[float | None] = mapped_column(Numeric(12, 2))
    sale_price:     Mapped[float | None] = mapped_column(Numeric(12, 2))
    cost_price:     Mapped[float | None] = mapped_column(Numeric(12, 2))
    tax_rate:       Mapped[float | None] = mapped_column(Numeric(5, 2))
    weight:         Mapped[float | None] = mapped_column(Numeric(8, 2))
    dimensions:     Mapped[str | None]   = mapped_column(String(50))

    product_status: Mapped[ProductStatusEnum] = mapped_column(
        Enum(ProductStatusEnum), default=ProductStatusEnum.draft, index=True
    )
    is_featured:    Mapped[bool] = mapped_column(Boolean, default=False)

    total_sales:    Mapped[int | None]   = mapped_column(Integer, default=0)
    total_revenue:  Mapped[float | None] = mapped_column(Numeric(12, 2), default=0)
    average_rating: Mapped[float | None] = mapped_column(Numeric(3, 2))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────────────────────
    seller:   Mapped["User | None"]     = relationship("User", back_populates="products")
    category: Mapped["Category | None"] = relationship("Category", back_populates="products")
    brand:    Mapped["Brand | None"]    = relationship("Brand", back_populates="products")

    variants:         Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="product", cascade="all, delete-orphan"
    )
    images:           Mapped[list["ProductImage"]] = relationship(
        "ProductImage", back_populates="product", cascade="all, delete-orphan"
    )
    attribute_values: Mapped[list["ProductAttributeValue"]] = relationship(
        "ProductAttributeValue", back_populates="product", cascade="all, delete-orphan"
    )
    tags:             Mapped[list["Tag"]] = relationship(
        "Tag", secondary=product_tags, back_populates="products"
    )
    reviews:          Mapped[list["Review"]] = relationship("Review", back_populates="product")
    questions:        Mapped[list["ProductQuestion"]] = relationship(
        "ProductQuestion", back_populates="product", cascade="all, delete-orphan"
    )
    order_items:      Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
    inventory:        Mapped[list["Inventory"]] = relationship("Inventory", back_populates="product")
    cart_items:       Mapped[list["ShoppingCart"]] = relationship(
        "ShoppingCart", back_populates="product"
    )
    purchase_order_items: Mapped[list["PurchaseOrderItem"]] = relationship(
        "PurchaseOrderItem", back_populates="product"
    )

    def __repr__(self) -> str:
        return f"<Product id={self.product_id} name={self.product_name!r}>"


class ProductVariant(Base):
    __tablename__ = "product_variants"

    variant_id:       Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    sku:              Mapped[str | None] = mapped_column(String(100), unique=True)
    variant_name:     Mapped[str | None] = mapped_column(String(100))
    price_adjustment: Mapped[float | None] = mapped_column(Numeric(12, 2), default=0)
    stock_quantity:   Mapped[int | None] = mapped_column(Integer, default=0)
    image_url:        Mapped[str | None] = mapped_column(String(255))
    is_active:        Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:       Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at:       Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────────────────────
    product:    Mapped["Product"] = relationship("Product", back_populates="variants")
    attributes: Mapped[list["VariantAttribute"]] = relationship(
        "VariantAttribute", back_populates="variant", cascade="all, delete-orphan"
    )
    order_items:Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="variant")
    inventory:  Mapped[list["Inventory"]] = relationship("Inventory", back_populates="variant")
    cart_items: Mapped[list["ShoppingCart"]] = relationship("ShoppingCart", back_populates="variant")
    purchase_order_items: Mapped[list["PurchaseOrderItem"]] = relationship(
        "PurchaseOrderItem", back_populates="variant"
    )

    def __repr__(self) -> str:
        return f"<ProductVariant id={self.variant_id} sku={self.sku!r}>"


class VariantAttribute(Base):
    __tablename__ = "variant_attributes"

    attribute_id:    Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("product_variants.variant_id", ondelete="CASCADE"), index=True
    )
    attribute_name:  Mapped[str | None] = mapped_column(String(50))
    attribute_value: Mapped[str | None] = mapped_column(String(100))

    # ── Relationships ────────────────────────────────────────────────────────
    variant: Mapped["ProductVariant"] = relationship("ProductVariant", back_populates="attributes")


class ProductImage(Base):
    __tablename__ = "product_images"

    image_id:      Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    image_url:     Mapped[str | None] = mapped_column(String(255))
    thumbnail_url: Mapped[str | None] = mapped_column(String(255))
    is_primary:    Mapped[bool] = mapped_column(Boolean, default=False)

    # ── Relationships ────────────────────────────────────────────────────────
    product: Mapped["Product"] = relationship("Product", back_populates="images")


class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    attribute_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("categories.category_id", ondelete="CASCADE"), index=True
    )
    attribute_name: Mapped[str | None] = mapped_column(String(100))
    attribute_type: Mapped[AttributeTypeEnum | None] = mapped_column(Enum(AttributeTypeEnum))
    is_filterable:  Mapped[bool] = mapped_column(Boolean, default=False)

    # ── Relationships ────────────────────────────────────────────────────────
    category: Mapped["Category | None"] = relationship(
        "Category", back_populates="product_attributes"
    )
    values: Mapped[list["ProductAttributeValue"]] = relationship(
        "ProductAttributeValue", back_populates="attribute"
    )


class ProductAttributeValue(Base):
    __tablename__ = "product_attribute_values"

    value_id:    Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    attribute_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("product_attributes.attribute_id", ondelete="CASCADE"), index=True
    )
    value: Mapped[str | None] = mapped_column(String(255))

    # ── Relationships ────────────────────────────────────────────────────────
    product:   Mapped["Product"]          = relationship("Product", back_populates="attribute_values")
    attribute: Mapped["ProductAttribute"] = relationship("ProductAttribute", back_populates="values")


class Tag(Base):
    __tablename__ = "tags"

    tag_id:   Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tag_name: Mapped[str] = mapped_column(String(50), unique=True)
    slug:     Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # ── Relationships ────────────────────────────────────────────────────────
    products: Mapped[list["Product"]] = relationship(
        "Product", secondary=product_tags, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag id={self.tag_id} name={self.tag_name!r}>"


class ProductQuestion(Base):
    __tablename__ = "product_questions"

    question_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.product_id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), index=True
    )
    question:   Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationships ────────────────────────────────────────────────────────
    product: Mapped["Product"] = relationship("Product", back_populates="questions")
    user:    Mapped["User | None"] = relationship("User", back_populates="questions")


# ── Lazy imports (circular reference prevention) ────────────────────────────────
from app.models.order     import OrderItem        # noqa: E402
from app.models.review    import Review           # noqa: E402
from app.models.inventory import Inventory        # noqa: E402
from app.models.cart      import ShoppingCart     # noqa: E402
from app.models.supply    import PurchaseOrderItem # noqa: E402
from app.models.user      import User             # noqa: E402
