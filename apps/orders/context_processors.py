"""
Context Processors — navbar uchun global ma'lumotlar
"""
from apps.orders.models import ShoppingCart
from apps.catalog.models import Category


def cart_count(request):
    """Barcha sahifalarda savat soni va nav kategoriyalarini ko'rsatish"""
    count = 0
    if request.user.is_authenticated:
        count = ShoppingCart.objects.filter(user=request.user).count()

    nav_cats = Category.objects.filter(
        is_active=True, parent__isnull=True
    ).order_by('category_name')[:8]

    return {
        'cart_count': count,
        'nav_categories': nav_cats,
    }
