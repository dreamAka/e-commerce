"""
Returns Models: Return, ReturnItem
"""
from django.db import models
from django.conf import settings


class Return(models.Model):
    class ReturnStatus(models.TextChoices):
        REQUESTED = 'requested', 'So\'ralgan'
        APPROVED = 'approved', 'Tasdiqlangan'
        REJECTED = 'rejected', 'Rad etilgan'
        RECEIVED = 'received', 'Qabul qilingan'
        REFUNDED = 'refunded', 'Qaytarilgan'

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='returns')
    return_status = models.CharField(max_length=10, choices=ReturnStatus.choices, default=ReturnStatus.REQUESTED)
    reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Qaytarish'
        verbose_name_plural = 'Qaytarishlar'

    def __str__(self):
        return f"Return #{self.id} — Order {self.order.order_number}"


class ReturnItem(models.Model):
    return_request = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items')
    order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Return item: {self.order_item.product.product_name} x{self.quantity}"
