"""
Catalog Serializers: Category, Brand, Product, HeroSection
"""
from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant, HeroSection


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'description', 'image_url', 'parent', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(product_status='active').count()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name', 'description', 'logo_url', 'country_of_origin']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'thumbnail_url', 'is_primary']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'variant_name', 'price_adjustment', 'stock_quantity', 'image_url']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', default=None)
    brand_name = serializers.CharField(source='brand.brand_name', default=None)
    current_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    primary_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'sku', 'base_price', 'sale_price',
            'current_price', 'discount_percent', 'average_rating', 'total_sales',
            'category_name', 'brand_name', 'primary_image_url', 'product_status',
        ]

    def get_primary_image_url(self, obj):
        img = obj.primary_image
        if img and img.image_url:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(img.image_url.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True, source='variants')
    current_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'sku', 'barcode', 'description',
            'base_price', 'sale_price', 'cost_price', 'current_price', 'discount_percent',
            'tax_rate', 'weight', 'dimensions', 'product_status', 'is_featured',
            'total_sales', 'average_rating', 'category', 'brand', 'images', 'variants',
            'created_at', 'updated_at',
        ]


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'subtitle', 'image', 'button_text', 'button_url', 'accent_color']
