from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.bookings.models import Booking
from .pdf_generator import generate_booking_itinerary_pdf

@login_required
def download_itinerary_pdf_view(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    
    # Permission check: customer can download if it's their booking or if staff/admin
    if booking.customer != request.user and not request.user.is_booking_staff and not request.user.is_admin_owner:
        messages.error(request, "You do not have permission to download this itinerary.")
        return redirect('bookings:my_bookings')

    pdf_buffer = generate_booking_itinerary_pdf(booking)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"JPT_Itinerary_{booking.reference_code}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response
