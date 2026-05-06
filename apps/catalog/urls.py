from django.urls import path
from apps.catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]
