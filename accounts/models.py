from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with a role so we can tell admins/managers apart from
    cashiers/waitstaff who should only see the POS screen."""

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CASHIER = 'CASHIER', 'Cashier'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CASHIER)
    phone = models.CharField(max_length=20, blank=True)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
