"""
Manager Panel Views — Dashboard, Orders, Products, Inventory, Users, Categories
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Count, Q, F, Avg
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from decimal import Decimal

from apps.accounts.decorators import admin_required
from apps.accounts.models import CustomUser
from apps.catalog.models import Product, Category, Brand, HeroSection, ProductImage
from apps.orders.models import Order, OrderItem, ShoppingCart
from apps.warehouse.models import Warehouse, Inventory, InventoryMovement
from apps.reviews.models import Review
from apps.returns.models import Return
from apps.suppliers.models import Supplier, PurchaseOrder


# ══════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════

@admin_required
def dashboard(request):
    today = timezone.now().date()
    last_30 = today - timedelta(days=30)

    # Stats
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(s=Sum('total_amount'))['s'] or 0
    total_products = Product.objects.filter(product_status='active').count()
    total_users = CustomUser.objects.filter(account_status='active').count()

    # Today
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = Order.objects.filter(created_at__date=today, payment_status='paid').aggregate(
        s=Sum('total_amount'))['s'] or 0

    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # Low stock
    low_stock = Inventory.objects.filter(quantity_available__lte=5).select_related('product', 'warehouse')[:10]

    # Pending reviews
    pending_reviews = Review.objects.filter(is_approved=False).count()

    # Pending returns
    pending_returns = Return.objects.filter(return_status='requested').count()

    # Chart data — last 7 days orders
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        chart_labels.append(d.strftime('%d/%m'))
        cnt = Order.objects.filter(created_at__date=d).count()
        chart_data.append(cnt)

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_users': total_users,
        'today_orders': today_orders,
        'today_revenue': today_revenue,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
        'pending_reviews': pending_reviews,
        'pending_returns': pending_returns,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'manager/dashboard.html', context)


# ══════════════════════════════════════════════════════════════
#  ORDERS
# ══════════════════════════════════════════════════════════════

@admin_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-created_at')

    # Filters
    status = request.GET.get('status')
    payment = request.GET.get('payment')
    search = request.GET.get('q', '')

    if status:
        orders = orders.filter(order_status=status)
    if payment:
        orders = orders.filter(payment_status=payment)
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search)
        )

    # Counts for badges
    counts = {
        'all': Order.objects.count(),
        'pending': Order.objects.filter(order_status='pending').count(),
        'processing': Order.objects.filter(order_status='processing').count(),
        'shipped': Order.objects.filter(order_status='shipped').count(),
        'delivered': Order.objects.filter(order_status='delivered').count(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('manager/partials/order_rows.html', {'orders': orders}, request=request)
        return JsonResponse({'html': html, 'counts': counts})

    return render(request, 'manager/order_list.html', {'orders': orders, 'counts': counts})


@admin_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user', 'shipping_address'), pk=order_id)
    items = order.items.select_related('product', 'variant')

    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        if new_status:
            order.order_status = new_status
            order.save()
            messages.success(request, f"Buyurtma statusi '{order.get_order_status_display()}' ga o'zgartirildi.")
            return redirect('manager:order_detail', order_id=order.pk)

    return render(request, 'manager/order_detail.html', {'order': order, 'items': items})


# ══════════════════════════════════════════════════════════════
#  PRODUCTS
# ══════════════════════════════════════════════════════════════

@admin_required
def product_list(request):
    products = Product.objects.select_related('category', 'brand').order_by('-created_at')

    search = request.GET.get('q', '')
    cat = request.GET.get('category')
    status = request.GET.get('status')

    if search:
        products = products.filter(
            Q(product_name__icontains=search) | Q(sku__icontains=search)
        )
    if cat:
        products = products.filter(category_id=cat)
    if status:
        products = products.filter(product_status=status)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('manager/partials/product_rows.html', {'products': products}, request=request)
        return JsonResponse({'html': html, 'count': products.count()})

    categories = Category.objects.filter(is_active=True)
    return render(request, 'manager/product_list.html', {
        'products': products,
        'categories': categories,
    })


@admin_required
def product_form(request, product_id=None):
    product = get_object_or_404(Product, pk=product_id) if product_id else None

    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        if product is None:
            product = Product()

        product.product_name = data.get('product_name', '')
        product.slug = data.get('slug', '')
        product.sku = data.get('sku', '')
        product.description = data.get('description', '')
        product.base_price = Decimal(data.get('base_price', '0'))
        product.sale_price = Decimal(data.get('sale_price', '0')) if data.get('sale_price') else None
        product.cost_price = Decimal(data.get('cost_price', '0')) if data.get('cost_price') else None
        product.category_id = data.get('category') or None
        product.brand_id = data.get('brand') or None
        product.product_status = data.get('product_status', 'draft')
        product.is_featured = data.get('is_featured') == 'on'
        product.save()

        # ── O'chiriladigan rasmlar ──
        delete_ids = data.getlist('delete_image')
        if delete_ids:
            ProductImage.objects.filter(pk__in=delete_ids, product=product).delete()

        # ── Yangi rasmlarni yuklash ──
        uploaded = files.getlist('images')
        for i, img_file in enumerate(uploaded):
            is_primary = (i == 0 and not product.images.filter(is_primary=True).exists())
            ProductImage.objects.create(
                product=product,
                image_url=img_file,
                is_primary=is_primary,
            )

        # ── Asosiy rasmni o'zgartirish ──
        primary_id = data.get('primary_image')
        if primary_id:
            product.images.update(is_primary=False)
            product.images.filter(pk=primary_id).update(is_primary=True)

        messages.success(request, f"Mahsulot '{product.product_name}' saqlandi.")
        return redirect('manager:product_list')

    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    existing_images = product.images.all() if product else []
    return render(request, 'manager/product_form.html', {
        'product': product,
        'categories': categories,
        'brands': brands,
        'existing_images': existing_images,
    })


@admin_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    name = product.product_name
    product.delete()
    messages.success(request, f"'{name}' o'chirildi.")
    return redirect('manager:product_list')


# ══════════════════════════════════════════════════════════════
#  INVENTORY
# ══════════════════════════════════════════════════════════════

@admin_required
def inventory_list(request):
    inventory = Inventory.objects.select_related('product', 'warehouse').order_by('product__product_name')

    search = request.GET.get('q', '')
    if search:
        inventory = inventory.filter(product__product_name__icontains=search)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('manager/partials/inventory_rows.html', {'inventory': inventory}, request=request)
        return JsonResponse({'html': html})

    warehouses = Warehouse.objects.filter(is_active=True)
    return render(request, 'manager/inventory_list.html', {'inventory': inventory, 'warehouses': warehouses})


# ══════════════════════════════════════════════════════════════
#  USERS
# ══════════════════════════════════════════════════════════════

@admin_required
def user_list(request):
    users = CustomUser.objects.order_by('-date_joined')

    search = request.GET.get('q', '')
    user_type = request.GET.get('type')

    if search:
        users = users.filter(
            Q(username__icontains=search) | Q(email__icontains=search) |
            Q(first_name__icontains=search) | Q(phone__icontains=search)
        )
    if user_type:
        users = users.filter(user_type=user_type)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('manager/partials/user_rows.html', {'users': users}, request=request)
        return JsonResponse({'html': html, 'count': users.count()})

    return render(request, 'manager/user_list.html', {'users': users})


@admin_required
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    orders = user.orders.order_by('-created_at')[:10]
    return render(request, 'manager/user_detail.html', {'profile_user': user, 'orders': orders})


@admin_required
def user_toggle_status(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if user.account_status == 'active':
        user.account_status = 'suspended'
        messages.warning(request, f"{user.username} bloklandi.")
    else:
        user.account_status = 'active'
        messages.success(request, f"{user.username} faollashtirildi.")
    user.save()
    return redirect('manager:user_detail', user_id=user.pk)


# ══════════════════════════════════════════════════════════════
#  CATEGORIES
# ══════════════════════════════════════════════════════════════

@admin_required
def category_list(request):
    categories = Category.objects.select_related('parent').order_by('category_name')
    return render(request, 'manager/category_list.html', {'categories': categories})


@admin_required
def category_form(request, category_id=None):
    category = get_object_or_404(Category, pk=category_id) if category_id else None

    if request.method == 'POST':
        data = request.POST
        if category is None:
            category = Category()
        category.category_name = data.get('category_name', '')
        category.slug = data.get('slug', '')
        category.description = data.get('description', '')
        category.is_active = data.get('is_active') == 'on'
        category.parent_id = data.get('parent') or None
        category.save()
        messages.success(request, f"Kategoriya '{category.category_name}' saqlandi.")
        return redirect('manager:category_list')

    parents = Category.objects.exclude(pk=category_id) if category_id else Category.objects.all()
    return render(request, 'manager/category_form.html', {'category': category, 'parents': parents})


# ══════════════════════════════════════════════════════════════
#  STOREFRONT (Hero sections — to'liq CRUD)
# ══════════════════════════════════════════════════════════════

@admin_required
def storefront_settings(request):
    heroes = HeroSection.objects.order_by('order')
    return render(request, 'manager/storefront_settings.html', {'heroes': heroes})


@admin_required
def hero_form(request, hero_id=None):
    hero = get_object_or_404(HeroSection, pk=hero_id) if hero_id else None

    if request.method == 'POST':
        data = request.POST
        if hero is None:
            hero = HeroSection()

        hero.title = data.get('title', '')
        hero.subtitle = data.get('subtitle', '')
        hero.button_text = data.get('button_text', 'Sotib Olish')
        hero.button_url = data.get('button_url', '#products')
        hero.accent_color = data.get('accent_color', '#44d62c')
        hero.order = int(data.get('order', 0))
        hero.is_active = data.get('is_active') == 'on'
        hero.save()

        # Rasm yuklash
        if request.FILES.get('image'):
            hero.image = request.FILES['image']
            hero.save()

        messages.success(request, f"Banner '{hero.title}' saqlandi.")
        return redirect('manager:storefront')

    return render(request, 'manager/hero_form.html', {
        'hero': hero,
        'preset_colors': ['#44d62c', '#00d4ff', '#ff4d4d', '#ff8c00', '#c084fc', '#ffffff'],
    })


@admin_required
def hero_delete(request, hero_id):
    hero = get_object_or_404(HeroSection, pk=hero_id)
    title = hero.title
    hero.delete()
    messages.success(request, f"'{title}' banneri o'chirildi.")
    return redirect('manager:storefront')


@admin_required
def hero_toggle(request, hero_id):
    hero = get_object_or_404(HeroSection, pk=hero_id)
    hero.is_active = not hero.is_active
    hero.save()
    status = "faollashtirildi" if hero.is_active else "o'chirildi"
    messages.success(request, f"Banner {status}.")
    return redirect('manager:storefront')

