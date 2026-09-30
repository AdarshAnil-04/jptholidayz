import uuid
import random
from django.db import models
from django.conf import settings
from apps.packages.models import TravelPackage

class Booking(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending Request'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        QUOTED = 'QUOTED', 'Quote Issued'
        AWAITING_PAYMENT = 'AWAITING_PAYMENT', 'Awaiting Payment'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    reference_code = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    # Guest details if submitted without logging in or for record
    guest_name = models.CharField(max_length=150)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=30)
    
    package = models.ForeignKey(TravelPackage, on_delete=models.PROTECT, related_name='bookings')
    travel_date = models.DateField(help_text='Preferred departure date')
    adults_count = models.PositiveIntegerField(default=1)
    children_count = models.PositiveIntegerField(default=0)
    
    # Financial snapshot (locked agreed amount so future package edits don't alter history)
    total_quoted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    pickup_location = models.CharField(max_length=255, blank=True)
    special_requests = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True, help_text='Staff notes (not visible to customer)')
    
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_bookings',
        limit_choices_to={'role__in': ['BOOKING_STAFF', 'SUPER_ADMIN']}
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking Request'
        verbose_name_plural = 'Booking Requests'

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = self.generate_reference_code()
        
        # Calculate initial estimated price if not set
        if self.total_quoted_price is None and self.package:
            # Estimate: price_per_person * (adults + 0.5 * children)
            estimated = float(self.package.price_per_person) * (self.adults_count + (0.5 * self.children_count))
            self.total_quoted_price = estimated

        super().save(*args, **kwargs)

    @classmethod
    def generate_reference_code(cls):
        prefix = "JPT"
        rand_digits = random.randint(10000, 99999)
        code = f"{prefix}-{rand_digits}"
        while cls.objects.filter(reference_code=code).exists():
            rand_digits = random.randint(10000, 99999)
            code = f"{prefix}-{rand_digits}"
        return code

    @property
    def total_travelers(self):
        return self.adults_count + self.children_count

    @property
    def amount_paid(self):
        payments = self.payment_records.filter(payment_status='VERIFIED')
        return sum(p.amount for p in payments) if payments.exists() else 0

    @property
    def amount_due(self):
        if self.total_quoted_price is None:
            return 0
        return max(0, float(self.total_quoted_price) - float(self.amount_paid))

    @property
    def is_fully_paid(self):
        return self.amount_due == 0 and self.total_quoted_price and self.total_quoted_price > 0

    def transition_to(self, new_status, user=None, note=''):
        old_status = self.status
        self.status = new_status
        self.save()
        BookingStatusHistory.objects.create(
            booking=self,
            from_status=old_status,
            to_status=new_status,
            changed_by=user,
            note=note
        )

    def __str__(self):
        return f"[{self.reference_code}] {self.package.title} - {self.guest_name} ({self.get_status_display()})"

class BookingStatusHistory(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Booking Status Histories'

    def __str__(self):
        return f"Booking {self.booking.reference_code}: {self.from_status} -> {self.to_status}"
