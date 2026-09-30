from django.db import models
from django.conf import settings
from apps.bookings.models import Booking

class PaymentRecord(models.Model):
    class PaymentMethod(models.TextChoices):
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Direct Wire / Transfer'
        CASH = 'CASH', 'Cash Payment'
        CREDIT_CARD = 'CREDIT_CARD', 'Credit / Debit Card'
        ONLINE_GATEWAY = 'ONLINE_GATEWAY', 'Online Gateway (Stripe/PayPal)'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Verification'
        VERIFIED = 'VERIFIED', 'Verified / Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payment_records')
    payment_reference = models.CharField(max_length=100, unique=True, help_text='Transaction ref or Bank receipt number')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.BANK_TRANSFER)
    payment_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    receipt_document = models.FileField(upload_to='receipts/', blank=True, null=True, help_text='Proof of payment upload')
    notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_payments'
    )
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Record'
        verbose_name_plural = 'Payment Records'

    def __str__(self):
        return f"Payment {self.payment_reference} - ${self.amount} for Booking {self.booking.reference_code} ({self.get_payment_status_display()})"
