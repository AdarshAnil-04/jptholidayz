from django.db import models
from django.conf import settings

class CustomEnquiry(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        IN_DISCUSSION = 'IN_DISCUSSION', 'In Discussion'
        QUOTE_SENT = 'QUOTE_SENT', 'Quote Sent'
        CONVERTED = 'CONVERTED', 'Converted to Booking'
        CLOSED = 'CLOSED', 'Closed'

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    destination_preference = models.CharField(max_length=150, help_text='Preferred destination or region')
    preferred_date = models.DateField(null=True, blank=True)
    duration_days = models.PositiveIntegerField(default=7, null=True, blank=True)
    travelers_count = models.PositiveIntegerField(default=2)
    budget_range = models.CharField(max_length=100, blank=True, help_text='e.g., $2000 - $5000')
    preferences = models.TextField(blank=True, help_text='Luxury, Adventure, Family-friendly, Honeymoon, etc.')
    message = models.TextField()
    
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_enquiries'
    )
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Custom Enquiry'
        verbose_name_plural = 'Custom Enquiries'

    def __str__(self):
        return f"Enquiry by {self.name} for {self.destination_preference} ({self.get_status_display()})"

class EnquiryCommunicationLog(models.Model):
    class Channel(models.TextChoices):
        EMAIL = 'EMAIL', 'Email'
        PHONE = 'PHONE', 'Phone Call'
        WHATSAPP = 'WHATSAPP', 'WhatsApp'
        INTERNAL = 'INTERNAL', 'Internal Note'

    enquiry = models.ForeignKey(CustomEnquiry, on_delete=models.CASCADE, related_name='communication_logs')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.EMAIL)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Communication Log ({self.channel}) - {self.enquiry.name}"
