from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.bookings.models import Booking
from .models import PaymentRecord

@login_required
def payment_instructions_view(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    
    # Permission check
    if booking.customer != request.user and not request.user.is_booking_staff and not request.user.is_admin_owner:
        messages.error(request, "Unauthorized access to payment information.")
        return redirect('bookings:my_bookings')

    if request.method == 'POST':
        payment_ref = request.POST.get('payment_reference', '').strip()
        amount = request.POST.get('amount', '0')
        method = request.POST.get('payment_method', 'BANK_TRANSFER')
        notes = request.POST.get('notes', '').strip()
        receipt = request.FILES.get('receipt_document')

        if not payment_ref:
            messages.error(request, "Payment reference is required.")
        else:
            try:
                payment = PaymentRecord.objects.create(
                    booking=booking,
                    payment_reference=payment_ref,
                    amount=float(amount),
                    payment_method=method,
                    payment_status=PaymentRecord.Status.PENDING,
                    receipt_document=receipt,
                    notes=notes,
                    transaction_date=booking.created_at.date()
                )
                
                # Update booking status to under review if pending
                if booking.status in [Booking.Status.QUOTED, Booking.Status.AWAITING_PAYMENT]:
                    booking.transition_to(Booking.Status.UNDER_REVIEW, user=request.user, note=f"Payment reference {payment_ref} submitted.")
                
                messages.success(request, f"Payment receipt (Ref: {payment_ref}) submitted for verification. Staff will verify shortly.")
                return redirect('bookings:detail', reference_code=booking.reference_code)
            except Exception as e:
                messages.error(request, f"Could not submit payment record: {str(e)}")

    context = {
        'booking': booking,
    }
    return render(request, 'payments/instructions.html', context)
