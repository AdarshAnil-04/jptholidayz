from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.packages.models import TravelPackage
from apps.core.models import Notification
from .models import Booking, BookingStatusHistory
from .forms import BookingRequestForm

def create_booking_view(request, package_slug):
    package = get_object_or_404(TravelPackage, slug=package_slug, status='PUBLISHED')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'guest_name': request.user.get_full_name() or request.user.username,
            'guest_email': request.user.email,
            'guest_phone': request.user.phone or '',
        }

    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.package = package
            if request.user.is_authenticated:
                booking.customer = request.user
            booking.status = Booking.Status.PENDING
            booking.save()

            # Record status history
            BookingStatusHistory.objects.create(
                booking=booking,
                from_status='DRAFT',
                to_status=Booking.Status.PENDING,
                changed_by=request.user if request.user.is_authenticated else None,
                note='Booking request submitted by customer.'
            )

            # Create notification for user if logged in
            if request.user.is_authenticated:
                Notification.objects.create(
                    user=request.user,
                    title="Booking Request Received",
                    message=f"Your booking request {booking.reference_code} for {package.title} has been received. Our team will review availability and confirm shortly.",
                    link=f"/bookings/{booking.reference_code}/"
                )

            messages.success(
                request,
                f"Your booking request (Ref: {booking.reference_code}) has been submitted successfully! "
                "Note: A booking request is not an automated confirmation; our travel desk will review and contact you."
            )
            return redirect('bookings:success', reference_code=booking.reference_code)
        else:
            messages.error(request, "Error submitting booking request. Please verify the form inputs.")
    else:
        form = BookingRequestForm(initial=initial_data)

    context = {
        'package': package,
        'form': form,
    }
    return render(request, 'bookings/create_booking.html', context)

def booking_success_view(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    # Protection check
    if booking.customer and request.user.is_authenticated and booking.customer != request.user and not request.user.is_booking_staff:
        messages.error(request, "Unauthorized access to booking details.")
        return redirect('core:home')

    return render(request, 'bookings/booking_success.html', {'booking': booking})

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('package', 'package__destination')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail_view(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    
    if booking.customer != request.user and not request.user.is_booking_staff and not request.user.is_admin_owner:
        messages.error(request, "You do not have permission to view this booking.")
        return redirect('bookings:my_bookings')

    history = booking.status_history.all()
    payments = booking.payment_records.all()

    context = {
        'booking': booking,
        'history': history,
        'payments': payments,
    }
    return render(request, 'bookings/booking_detail.html', context)
