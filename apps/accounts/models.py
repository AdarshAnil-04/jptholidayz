from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin / Owner'
        BOOKING_STAFF = 'BOOKING_STAFF', 'Booking Staff'
        CONTENT_MANAGER = 'CONTENT_MANAGER', 'Content Manager'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        help_text='User authorization role'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    @property
    def is_booking_staff(self):
        return self.role in [self.Role.BOOKING_STAFF, self.Role.SUPER_ADMIN] or self.is_superuser

    @property
    def is_content_manager(self):
        return self.role in [self.Role.CONTENT_MANAGER, self.Role.SUPER_ADMIN] or self.is_superuser

    @property
    def is_admin_owner(self):
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.SUPER_ADMIN
        super().save(*args, **kwargs)

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    travel_preferences = models.TextField(blank=True, null=True, help_text='Preferred travel style, dietary requests, etc.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer Profile: {self.user.get_full_name() or self.user.username}"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100, default='Travel Operations')
    job_title = models.CharField(max_length=100, default='Travel Consultant')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Staff Profile: {self.user.username} ({self.employee_id})"
