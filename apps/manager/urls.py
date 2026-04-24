from django.urls import path
from apps.manager import views

app_name = 'manager'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_form, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_form, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),

    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),

    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/toggle/', views.user_toggle_status, name='user_toggle'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_form, name='category_add'),
    path('categories/<int:category_id>/edit/', views.category_form, name='category_edit'),

    # Storefront / Hero Bannerlar
    path('storefront/', views.storefront_settings, name='storefront'),
    path('storefront/hero/add/', views.hero_form, name='hero_add'),
    path('storefront/hero/<int:hero_id>/edit/', views.hero_form, name='hero_edit'),
    path('storefront/hero/<int:hero_id>/delete/', views.hero_delete, name='hero_delete'),
    path('storefront/hero/<int:hero_id>/toggle/', views.hero_toggle, name='hero_toggle'),
]
