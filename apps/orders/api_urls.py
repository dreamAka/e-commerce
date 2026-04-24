from django.urls import path
from . import api_views

urlpatterns = [
    path('cart/', api_views.api_cart, name='api-cart'),
    path('orders/', api_views.api_orders, name='api-orders'),
    path('wishlist/', api_views.api_wishlist, name='api-wishlist'),
]
