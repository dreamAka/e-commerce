from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CategoryViewSet, BrandViewSet, ProductViewSet, HeroViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api-categories')
router.register('brands', BrandViewSet, basename='api-brands')
router.register('products', ProductViewSet, basename='api-products')
router.register('heroes', HeroViewSet, basename='api-heroes')

urlpatterns = [
    path('', include(router.urls)),
]
