from django.contrib import admin
from .models import Booking, BookingStatusHistory

class BookingStatusHistoryInline(admin.TabularInline):
    model = BookingStatusHistory
    readonly_fields = ('from_status', 'to_status', 'changed_by', 'note', 'timestamp')
    extra = 0
    can_delete = False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'guest_name', 'package', 'travel_date', 'total_quoted_price', 'status', 'created_at')
    list_filter = ('status', 'travel_date', 'created_at')
    search_fields = ('reference_code', 'guest_name', 'guest_email', 'guest_phone', 'package__title')
    readonly_fields = ('reference_code', 'created_at', 'updated_at')
    inlines = [BookingStatusHistoryInline]
