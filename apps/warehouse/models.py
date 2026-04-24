"""
Warehouse Models: Warehouse, Inventory, InventoryMovement
"""
from django.db import models
from django.conf import settings


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ombor'
        verbose_name_plural = 'Omborlar'

    def __str__(self):
        return self.warehouse_name


class Inventory(models.Model):
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='inventory')
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory')
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    quantity_damaged = models.IntegerField(default=0)
    last_restock_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Zaxira'
        verbose_name_plural = 'Zaxiralar'
        unique_together = ('product', 'variant', 'warehouse')

    def __str__(self):
        return f"{self.product.product_name} @ {self.warehouse.warehouse_name}: {self.quantity_available}"


class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'in', 'Kirim'
        OUT = 'out', 'Chiqim'
        ADJUSTMENT = 'adjustment', 'Tuzatish'
        RETURN = 'return', 'Qaytarish'
        DAMAGE = 'damage', 'Zarar'

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=15, choices=MovementType.choices)
    quantity = models.IntegerField()
    reference_type = models.CharField(max_length=50, blank=True)
    reference_id = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ombor Harakati'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()}: {self.quantity}"
