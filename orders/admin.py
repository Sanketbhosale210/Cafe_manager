from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'payment_method', 'table_number', 'created_by', 'created_at')
    list_filter = ('status', 'payment_method')
    inlines = [OrderItemInline]
