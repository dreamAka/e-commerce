"""
Catalog Views: Home, Product List, Product Detail
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

from .models import Product, Category, Brand, HeroSection, Wishlist


def home(request):
    heroes = HeroSection.objects.filter(is_active=True).order_by('order')
    featured = Product.objects.filter(is_featured=True, product_status='active').select_related('category', 'brand')[:8]
    categories = Category.objects.filter(is_active=True, parent__isnull=True)[:6]
    brands = Brand.objects.filter(is_active=True)[:8]

    return render(request, 'home.html', {
        'heroes': heroes,
        'featured_products': featured,
        'categories': categories,
        'brands': brands,
    })


def product_list(request):
    products = Product.objects.filter(product_status='active').select_related('category', 'brand')

    # Search
    q = request.GET.get('q', '')
    if q:
        products = products.filter(
            Q(product_name__icontains=q) | Q(description__icontains=q) | Q(sku__icontains=q)
        )

    # Category filter
    cat_slug = request.GET.get('category')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    # Brand filter
    brand_id = request.GET.get('brand')
    if brand_id:
        products = products.filter(brand_id=brand_id)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'price_asc': 'base_price',
        'price_desc': '-base_price',
        'name': 'product_name',
        'newest': '-created_at',
        'popular': '-total_sales',
        'rating': '-average_rating',
    }
    products = products.order_by(valid_sorts.get(sort, '-created_at'))

    # AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('catalog/partials/product_cards.html', {'products': products}, request=request)
        return JsonResponse({'html': html, 'count': products.count()})

    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_q': q,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand', 'seller'),
        slug=slug, product_status='active'
    )
    images = product.images.all()
    variants = product.variants.filter(is_active=True)
    reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')[:10]
    related = Product.objects.filter(
        category=product.category, product_status='active'
    ).exclude(pk=product.pk)[:4]

    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'images': images,
        'variants': variants,
        'reviews': reviews,
        'related': related,
        'is_wishlisted': is_wishlisted,
    })
