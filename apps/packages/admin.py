from django.contrib import admin
from .models import TravelPackage, PackageImage, ItineraryDay

class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1

class ItineraryDayInline(admin.StackedInline):
    model = ItineraryDay
    extra = 1

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'duration_days', 'duration_nights', 'price_per_person', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'destination', 'pricing_basis')
    search_fields = ('title', 'overview', 'inclusions', 'exclusions')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PackageImageInline, ItineraryDayInline]
