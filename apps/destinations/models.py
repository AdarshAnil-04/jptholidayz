from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Destination(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    country = models.CharField(max_length=100, default='Global')
    tagline = models.CharField(max_length=255, blank=True, help_text='Short catchy headline for cards')
    description = models.TextField(help_text='Detailed destination overview')
    cover_image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text='Show on homepage featured destinations section')
    is_published = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} Travel Packages & Holidays - JPT Holidays"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('destinations:detail', kwargs={'slug': self.slug})

    @property
    def package_count(self):
        return self.packages.filter(status='PUBLISHED').count()

    def __str__(self):
        return f"{self.name} ({self.country})"
