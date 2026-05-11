"""
Orders Views: Cart, Checkout, Order History
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import ShoppingCart, Order, OrderItem
from apps.catalog.models import Product


@login_required
def cart_view(request):
    cart_items = ShoppingCart.objects.filter(user=request.user).select_related('product', 'variant')

    total = sum(
        (item.product.current_price + (item.variant.price_adjustment if item.variant else 0)) * item.quantity
        for item in cart_items
    )

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, product_status='active')
    qty = int(request.POST.get('quantity', 1))

    # Check stock
    existing = ShoppingCart.objects.filter(user=request.user, product=product, variant=None).first()
    current_in_cart = existing.quantity if existing else 0
    
    if product.stock_quantity <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': "Bu mahsulot omborda tugagan."})
        messages.error(request, "Bu mahsulot omborda tugagan.")
        return redirect('orders:cart')
    
    if current_in_cart + qty > product.stock_quantity:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f"Omborda faqat {product.stock_quantity} ta mavjud."})
        messages.error(request, f"Omborda faqat {product.stock_quantity} ta mavjud.")
        return redirect('orders:cart')

    if existing:
        existing.quantity += qty
        existing.save()
    else:
        ShoppingCart.objects.create(user=request.user, product=product, variant=None, quantity=qty)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = ShoppingCart.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'cart_count': count})

    messages.success(request, f"'{product.product_name}' savatga qo'shildi!")
    return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(ShoppingCart, pk=item_id, user=request.user)
    item.delete()
    messages.success(request, "Mahsulot savatdan o'chirildi.")
    return redirect('orders:cart')


@login_required
def checkout_view(request):
    cart_items = ShoppingCart.objects.filter(user=request.user).select_related('product', 'variant')
    if not cart_items.exists():
        messages.warning(request, "Savatingiz bo'sh.")
        return redirect('orders:cart')

    total = sum(
        (item.product.current_price + (item.variant.price_adjustment if item.variant else 0)) * item.quantity
        for item in cart_items
    )

    if request.method == 'POST':
        # Handle shipping address
        shipping_addr = None
        use_new = request.POST.get('use_new_address') == '1'

        if use_new:
            # Create new address from form
            from apps.accounts.models import Address
            new_name = request.POST.get('new_full_name', '').strip()
            new_phone = request.POST.get('new_phone', '').strip()
            new_region = request.POST.get('new_region', '').strip()
            new_city = request.POST.get('new_city', '').strip()
            new_district = request.POST.get('new_district', '').strip()
            new_street = request.POST.get('new_street', '').strip()
            new_postal = request.POST.get('new_postal_code', '').strip()

            if new_name and new_phone and new_region and new_city and new_street:
                shipping_addr = Address.objects.create(
                    user=request.user,
                    full_name=new_name,
                    phone=new_phone,
                    region=new_region,
                    city=new_city,
                    district=new_district,
                    street_address=new_street,
                    postal_code=new_postal,
                    is_default=not request.user.addresses.exists(),
                )
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': "Iltimos, barcha majburiy manzil maydonlarini to'ldiring."})
                messages.error(request, "Iltimos, barcha majburiy manzil maydonlarini to'ldiring.")
                addresses = request.user.addresses.all()
                return render(request, 'orders/checkout.html', {
                    'cart_items': cart_items, 'total': total, 'addresses': addresses,
                })
        else:
            addr_id = request.POST.get('shipping_address')
            if addr_id:
                shipping_addr = request.user.addresses.filter(pk=addr_id).first()

            if not shipping_addr:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': "Iltimos, yetkazish manzilini tanlang yoki yangi manzil kiriting."})
                messages.error(request, "Iltimos, yetkazish manzilini tanlang yoki yangi manzil kiriting.")
                addresses = request.user.addresses.all()
                return render(request, 'orders/checkout.html', {
                    'cart_items': cart_items, 'total': total, 'addresses': addresses,
                })

        # Create order
        order = Order.objects.create(
            user=request.user,
            subtotal=total,
            total_amount=total,
            payment_method=request.POST.get('payment_method', 'naqd'),
            notes=request.POST.get('notes', ''),
            shipping_address=shipping_addr,
        )

        # Create order items
        for item in cart_items:
            price = item.product.current_price + (item.variant.price_adjustment if item.variant else 0)
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                unit_price=price,
                subtotal=price * item.quantity,
            )

        # Clear cart
        cart_items.delete()

        # Update product sales
        for oi in order.items.all():
            oi.product.total_sales += oi.quantity
            oi.product.save()

        # AJAX request — return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'order_number': order.order_number,
                'order_id': order.pk,
            })

        messages.success(request, f"Buyurtma #{order.order_number} yaratildi!")
        return redirect('orders:order_detail', order_id=order.pk)

    addresses = request.user.addresses.all()
    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'addresses': addresses,
    })


@login_required
def order_list(request):
    orders = request.user.orders.order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    items = order.items.select_related('product', 'variant')
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})


@login_required
def order_receipt(request, order_id):
    """Buyurtma cheki — yangi tabda ochiladi (print uchun)"""
    order = get_object_or_404(
        Order.objects.select_related('user', 'shipping_address'),
        pk=order_id, user=request.user
    )
    items = order.items.select_related('product', 'variant')
    return render(request, 'orders/receipt.html', {
        'order': order,
        'items': items,
    })
