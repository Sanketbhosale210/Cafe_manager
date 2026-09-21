from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CafeUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Cafe role', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Cafe role', {'fields': ('role', 'phone')}),
    )
    list_display = ('username', 'get_full_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
