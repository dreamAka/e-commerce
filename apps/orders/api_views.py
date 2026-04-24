"""
Orders API Views: Cart, Orders, Wishlist
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import ShoppingCart, Order
from .serializers import CartSerializer, OrderSerializer
from apps.catalog.models import Product, Wishlist


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def api_cart(request):
    if request.method == 'GET':
        items = ShoppingCart.objects.filter(user=request.user).select_related('product')
        return Response(CartSerializer(items, many=True).data)

    if request.method == 'POST':
        product_id = request.data.get('product_id')
        qty = int(request.data.get('quantity', 1))
        product = Product.objects.filter(pk=product_id, product_status='active').first()
        if not product:
            return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        item, created = ShoppingCart.objects.get_or_create(
            user=request.user, product=product, variant=None,
            defaults={'quantity': qty}
        )
        if not created:
            item.quantity += qty
            item.save()
        return Response(CartSerializer(item).data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        item_id = request.data.get('item_id')
        ShoppingCart.objects.filter(pk=item_id, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_orders(request):
    orders = request.user.orders.order_by('-created_at')
    return Response(OrderSerializer(orders, many=True).data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def api_wishlist(request):
    if request.method == 'GET':
        items = Wishlist.objects.filter(user=request.user).select_related('product')
        data = [{'id': w.id, 'product_id': w.product_id, 'product_name': w.product.product_name,
                 'added_at': w.added_at} for w in items]
        return Response(data)

    if request.method == 'POST':
        product_id = request.data.get('product_id')
        Wishlist.objects.get_or_create(user=request.user, product_id=product_id)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        product_id = request.data.get('product_id')
        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
