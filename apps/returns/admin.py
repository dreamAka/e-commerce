from django.contrib import admin
from .models import Return, ReturnItem

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'return_status', 'refund_amount', 'created_at')
    list_filter = ('return_status',)

admin.site.register(ReturnItem)
