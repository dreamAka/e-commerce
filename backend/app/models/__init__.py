"""
Models package – import all models here so SQLAlchemy
registers them before create_all() is called.
"""

# Correct import order prevents circular-reference issues.
# Base → simple models first → models with FK deps next.

from app.models.product   import (       # noqa: F401
    Category, Brand, Product,
    ProductVariant, VariantAttribute,
    ProductImage,
    ProductAttribute, ProductAttributeValue,
    Tag, ProductQuestion,
    product_tags,
)
from app.models.user      import (       # noqa: F401
    User, Address, UserSession,
    PasswordResetToken, EmailVerificationToken,
)
from app.models.order     import (       # noqa: F401
    Order, OrderItem, PaymentTransaction,
)
from app.models.review    import (       # noqa: F401
    Review, ReviewImage, ReviewReaction,
)
from app.models.inventory import (       # noqa: F401
    Warehouse, Inventory, InventoryMovement,
)
from app.models.supply    import (       # noqa: F401
    Supplier, PurchaseOrder, PurchaseOrderItem,
)
from app.models.returns   import (       # noqa: F401
    Return, ReturnItem,
)
from app.models.cart      import (       # noqa: F401
    ShoppingCart,
)

__all__ = [
    # Catalog
    "Category", "Brand", "Product",
    "ProductVariant", "VariantAttribute",
    "ProductImage",
    "ProductAttribute", "ProductAttributeValue",
    "Tag", "ProductQuestion", "product_tags",
    # Users & Auth
    "User", "Address", "UserSession",
    "PasswordResetToken", "EmailVerificationToken",
    # Orders & Payments
    "Order", "OrderItem", "PaymentTransaction",
    # Reviews
    "Review", "ReviewImage", "ReviewReaction",
    # Inventory
    "Warehouse", "Inventory", "InventoryMovement",
    # Supply chain
    "Supplier", "PurchaseOrder", "PurchaseOrderItem",
    # Returns
    "Return", "ReturnItem",
    # Cart
    "ShoppingCart",
]
