"""
Catalog API Views
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from .models import Category, Brand, Product, HeroSection
from .serializers import (CategorySerializer, BrandSerializer,
                          ProductListSerializer, ProductDetailSerializer, HeroSectionSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(product_status='active').select_related('category', 'brand')
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'description', 'sku']
    ordering_fields = ['base_price', 'created_at', 'total_sales', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        featured = self.request.query_params.get('featured')

        if category:
            qs = qs.filter(category__slug=category)
        if brand:
            qs = qs.filter(brand_id=brand)
        if featured:
            qs = qs.filter(is_featured=True)
        return qs


class HeroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HeroSection.objects.filter(is_active=True).order_by('order')
    serializer_class = HeroSectionSerializer
    permission_classes = [AllowAny]
