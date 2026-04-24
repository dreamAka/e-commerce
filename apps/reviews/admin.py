from django.contrib import admin
from .models import Review, ReviewImage, ReviewReaction

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    inlines = [ReviewImageInline]

admin.site.register(ReviewReaction)
