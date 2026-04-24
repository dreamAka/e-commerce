"""
Orders Serializers: Order, Cart, Wishlist
"""
from rest_framework import serializers
from .models import Order, OrderItem, ShoppingCart
from apps.catalog.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'variant', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_status_display = serializers.CharField(source='get_order_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'order_status', 'order_status_display',
                  'payment_status', 'payment_status_display', 'subtotal', 'total_amount',
                  'payment_method', 'notes', 'items', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_price = serializers.DecimalField(source='product.current_price', max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'product', 'product_name', 'product_price', 'variant', 'quantity', 'added_at']
