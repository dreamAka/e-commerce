from django.contrib import admin
from .models import (Category, Brand, Product, ProductVariant, VariantAttribute,
                     ProductImage, ProductAttribute, ProductAttributeValue,
                     Tag, ProductQuestion, Wishlist, HeroSection)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('category_name',)}
    list_filter = ('is_active',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'country_of_origin', 'is_active')
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'brand', 'base_price', 'sale_price',
                    'product_status', 'is_featured', 'total_sales')
    list_filter = ('product_status', 'category', 'brand', 'is_featured')
    search_fields = ('product_name', 'sku', 'description')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'slug')
    prepopulated_fields = {'slug': ('tag_name',)}


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'is_active', 'order')
    list_filter = ('is_active',)
    raw_id_fields = ('product',)


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at')


admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Wishlist)
