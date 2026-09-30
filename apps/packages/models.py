from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from apps.destinations.models import Destination

class TravelPackage(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    class PricingBasis(models.TextChoices):
        PER_PERSON = 'PER_PERSON', 'Per Person'
        PER_COUPLE = 'PER_COUPLE', 'Per Couple'
        PER_GROUP = 'PER_GROUP', 'Per Group'

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    overview = models.TextField(help_text='Detailed overview of what makes this holiday special')
    duration_days = models.PositiveIntegerField(default=5)
    duration_nights = models.PositiveIntegerField(default=4)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, help_text='Starting price per traveler')
    pricing_basis = models.CharField(max_length=20, choices=PricingBasis.choices, default=PricingBasis.PER_PERSON)
    cover_image = models.ImageField(upload_to='packages/covers/', blank=True, null=True)
    inclusions = models.TextField(help_text='List of items included (one per line or JSON format)')
    exclusions = models.TextField(help_text='List of items excluded (one per line or JSON format)')
    travel_requirements = models.TextField(blank=True, help_text='Passport, visa, health or travel insurance details')
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Travel Package'
        verbose_name_plural = 'Travel Packages'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while TravelPackage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('packages:detail', kwargs={'slug': self.slug})

    @property
    def inclusions_list(self):
        if not self.inclusions:
            return []
        return [item.strip() for item in self.inclusions.splitlines() if item.strip()]

    @property
    def exclusions_list(self):
        if not self.exclusions:
            return []
        return [item.strip() for item in self.exclusions.splitlines() if item.strip()]

    def __str__(self):
        return f"{self.title} ({self.duration_days}D/{self.duration_nights}N)"

class PackageImage(models.Model):
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='packages/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_cover = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.package.title} ({self.caption or 'No caption'})"

class ItineraryDay(models.Model):
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='itinerary_days')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, help_text='e.g., Arrival in Bali & Sunset Dinner')
    description = models.TextField()
    activities = models.TextField(blank=True, help_text='Key activities scheduled for the day')
    meals = models.CharField(max_length=100, blank=True, help_text='e.g., Breakfast, Dinner')
    accommodation = models.CharField(max_length=150, blank=True, help_text='Hotel / Resort stay info')
    transport = models.CharField(max_length=150, blank=True, help_text='Private Coach, Speedboat, Flight')

    class Meta:
        ordering = ['day_number']
        unique_together = ['package', 'day_number']

    def __str__(self):
        return f"Day {self.day_number}: {self.title} ({self.package.title})"
