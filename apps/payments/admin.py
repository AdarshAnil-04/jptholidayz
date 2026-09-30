from django.contrib import admin
from .models import PaymentRecord

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('payment_reference', 'booking', 'amount', 'payment_method', 'payment_status', 'verified_by', 'transaction_date')
    list_filter = ('payment_status', 'payment_method', 'transaction_date')
    search_fields = ('payment_reference', 'booking__reference_code', 'booking__guest_name')
