from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, SiteSettings, UserSession


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'account_status', 'loyalty_points', 'date_joined')
    list_filter = ('user_type', 'account_status', 'is_active')
    search_fields = ('username', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('NexGear', {'fields': ('phone', 'user_type', 'account_status', 'profile_image_url',
                                'loyalty_points', 'lifetime_value', 'customer_segment')}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'region', 'user', 'is_default')
    list_filter = ('region', 'address_type')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_domain', 'contact_phone')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'device_type', 'created_at')
