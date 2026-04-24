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

    cart_item, created = ShoppingCart.objects.get_or_create(
        user=request.user, product=product, variant=None,
        defaults={'quantity': qty}
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

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
        # Create order
        order = Order.objects.create(
            user=request.user,
            subtotal=total,
            total_amount=total,
            payment_method=request.POST.get('payment_method', 'naqd'),
            notes=request.POST.get('notes', ''),
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
