"""
Catalog Views: Home, Product List, Product Detail
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Brand, HeroSection, Wishlist


def home(request):
    heroes = HeroSection.objects.filter(is_active=True).select_related('product').order_by('order')
    featured = Product.objects.filter(is_featured=True, product_status='active').select_related('category', 'brand')[:8]
    categories = Category.objects.filter(is_active=True, parent__isnull=True)[:6]
    brands = Brand.objects.filter(is_active=True)[:8]

    return render(request, 'home.html', {
        'heroes': heroes,
        'featured_products': featured,
        'categories': categories,
        'brands': brands,
    })


@never_cache
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
        'current_cat': cat_slug or '',
        'current_brand': brand_id or '',
    })


from apps.reviews.models import Review
from apps.orders.models import OrderItem

def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand', 'seller'),
        slug=slug, product_status='active'
    )
    
    # Handle Review POST
    if request.method == 'POST' and request.user.is_authenticated:
        action = request.POST.get('action')
        if action == 'add_review':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '').strip()
            if rating and rating.isdigit():
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=int(rating),
                    comment=comment,
                    is_approved=True  # Auto-approve for demo
                )
                from django.contrib import messages
                messages.success(request, "Sharhingiz qo'shildi!")
                return redirect('catalog:product_detail', slug=product.slug)

    images = product.images.all()
    variants = product.variants.filter(is_active=True)
    reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')[:10]
    related = Product.objects.filter(
        category=product.category, product_status='active'
    ).exclude(pk=product.pk)[:4]

    is_wishlisted = False
    has_purchased = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, product=product).exists()
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product
        ).exists()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'images': images,
        'variants': variants,
        'reviews': reviews,
        'related': related,
        'is_wishlisted': is_wishlisted,
        'has_purchased': has_purchased,
    })


def search_suggestions(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'products': []})

    products = Product.objects.filter(
        Q(product_status='active') &
        (Q(product_name__icontains=q) | Q(brand__brand_name__icontains=q))
    ).select_related('brand').prefetch_related('images')[:5]

    from django.urls import reverse
    
    results = []
    for p in products:
        img_url = ''
        if p.images.exists():
            img_url = p.images.first().image_url.url
            
        results.append({
            'name': p.product_name,
            'url': reverse('catalog:product_detail', args=[p.slug]),
            'price': float(p.sale_price) if p.sale_price else float(p.base_price),
            'image': img_url,
        })
        
    return JsonResponse({'products': results})


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    products = [item.product for item in wishlist_items]
    return render(request, 'catalog/wishlist.html', {'products': products})
