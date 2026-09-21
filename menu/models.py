from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True, help_text="Uncheck to hide from the POS screen without deleting it.")
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional link to an inventory ingredient so selling this item can
    # automatically deduct stock (e.g. "Cappuccino" -> "Milk (L)").
    stock_item = models.ForeignKey(
        'inventory.StockItem', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='menu_items',
        help_text="Optional: pick a stock item to deduct one unit from every time this is sold."
    )

    class Meta:
        ordering = ['category__name', 'name']

    def __str__(self):
        return self.name
