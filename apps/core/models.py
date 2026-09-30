from django.db import models
from django.conf import settings

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='JPT Holidays')
    tagline = models.CharField(max_length=255, default='Your Trusted Travel & Bespoke Holiday Partner')
    contact_email = models.EmailField(default='info@jptholidays.placeholder')
    contact_phone = models.CharField(max_length=50, default='+1 (555) JPT-HOLIDAY [Placeholder]')
    whatsapp_number = models.CharField(max_length=50, default='+1 (555) 019-2834 [Placeholder]')
    office_address = models.TextField(default='123 Premium Travel Way, Tourism District [Placeholder]')
    business_hours = models.CharField(max_length=100, default='Mon - Sat: 9:00 AM - 6:00 PM EST')
    currency_code = models.CharField(max_length=10, default='USD')
    currency_symbol = models.CharField(max_length=5, default='$')
    facebook_url = models.URLField(blank=True, default='https://facebook.com/jptholidays.placeholder')
    instagram_url = models.URLField(blank=True, default='https://instagram.com/jptholidays.placeholder')
    twitter_url = models.URLField(blank=True, default='https://twitter.com/jptholidays.placeholder')
    youtube_url = models.URLField(blank=True, default='https://youtube.com/jptholidays.placeholder')
    about_text = models.TextField(default='JPT Holidays provides tailored travel experiences, luxury destination packages, and custom itineraries for travelers around the globe.')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_name

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.user} - {self.action} on {self.model_name}"
