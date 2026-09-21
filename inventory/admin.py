from django.contrib import admin
from .models import StockItem, StockMovement


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'reorder_level', 'is_low')
    list_filter = ('unit',)
    search_fields = ('name',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('stock_item', 'change', 'reason', 'created_by', 'created_at')
    list_filter = ('reason',)
