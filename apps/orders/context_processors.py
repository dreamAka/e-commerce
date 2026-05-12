"""
Context Processors — navbar uchun global ma'lumotlar
"""
from apps.orders.models import ShoppingCart
from apps.catalog.models import Category, Brand


def cart_count(request):
    """Barcha sahifalarda savat soni, nav kategoriyalari va brendlarini ko'rsatish"""
    count = 0
    if request.user.is_authenticated:
        count = ShoppingCart.objects.filter(user=request.user).count()

    nav_cats = Category.objects.filter(
        is_active=True, parent__isnull=True
    ).order_by('category_name')[:8]

    nav_brands = Brand.objects.filter(is_active=True).order_by('brand_name')[:8]

    return {
        'cart_count': count,
        'nav_categories': nav_cats,
        'nav_brands': nav_brands,
    }
