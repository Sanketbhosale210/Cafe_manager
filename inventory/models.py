from django.db import models
from django.conf import settings


class StockItem(models.Model):
    class Unit(models.TextChoices):
        PIECE = 'pc', 'pc'
        KG = 'kg', 'kg'
        GRAM = 'g', 'g'
        LITRE = 'L', 'L'
        ML = 'ml', 'ml'
        PACK = 'pack', 'pack'

    name = models.CharField(max_length=150, unique=True)
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.PIECE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reorder_level = models.DecimalField(
        max_digits=10, decimal_places=2, default=5,
        help_text="Alert when quantity falls to or below this level."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    @property
    def is_low(self):
        return self.quantity <= self.reorder_level


class StockMovement(models.Model):
    """Audit trail of every stock change: manual restock, sale deduction, or
    a manual correction/wastage entry."""

    class Reason(models.TextChoices):
        RESTOCK = 'RESTOCK', 'Restock'
        SALE = 'SALE', 'Sale deduction'
        ADJUSTMENT = 'ADJUSTMENT', 'Manual adjustment'
        WASTAGE = 'WASTAGE', 'Wastage / spoilage'

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='movements')
    change = models.DecimalField(max_digits=10, decimal_places=2, help_text="Positive to add stock, negative to remove.")
    reason = models.CharField(max_length=20, choices=Reason.choices, default=Reason.ADJUSTMENT)
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.stock_item.name}: {self.change:+} ({self.reason})"
