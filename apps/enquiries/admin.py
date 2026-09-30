from django.contrib import admin
from .models import CustomEnquiry, EnquiryCommunicationLog

class EnquiryCommunicationLogInline(admin.TabularInline):
    model = EnquiryCommunicationLog
    extra = 1

@admin.register(CustomEnquiry)
class CustomEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination_preference', 'travelers_count', 'budget_range', 'status', 'assigned_staff', 'created_at')
    list_filter = ('status', 'assigned_staff', 'created_at')
    search_fields = ('name', 'email', 'phone', 'destination_preference', 'message')
    inlines = [EnquiryCommunicationLogInline]
