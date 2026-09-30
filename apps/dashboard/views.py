from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from apps.accounts.decorators import booking_staff_required, content_manager_required, admin_required
from apps.accounts.models import User
from apps.destinations.models import Destination
from apps.packages.models import TravelPackage, PackageImage, ItineraryDay
from apps.bookings.models import Booking, BookingStatusHistory
from apps.enquiries.models import CustomEnquiry, EnquiryCommunicationLog
from apps.payments.models import PaymentRecord
from apps.gallery.models import GalleryImage, GalleryCategory
from apps.core.models import SiteSettings, AuditLog, Notification

@login_required
def dashboard_index_view(request):
    user = request.user
    if not (user.is_booking_staff or user.is_content_manager or user.is_admin_owner):
        return redirect('accounts:profile')

    total_packages = TravelPackage.objects.count()
    published_packages = TravelPackage.objects.filter(status='PUBLISHED').count()
    pending_bookings = Booking.objects.filter(status__in=['PENDING', 'UNDER_REVIEW']).count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    new_enquiries = CustomEnquiry.objects.filter(status='NEW').count()
    
    total_revenue = PaymentRecord.objects.filter(payment_status='VERIFIED').aggregate(total=Sum('amount'))['total'] or 0

    recent_bookings = Booking.objects.select_related('package', 'customer')[:5]
    recent_enquiries = CustomEnquiry.objects.all()[:5]

    context = {
        'total_packages': total_packages,
        'published_packages': published_packages,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'new_enquiries': new_enquiries,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'recent_enquiries': recent_enquiries,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
@booking_staff_required
def dashboard_bookings_view(request):
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()

    bookings = Booking.objects.select_related('package', 'customer', 'assigned_staff')

    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if query:
        bookings = bookings.filter(reference_code__icontains=query) | bookings.filter(guest_name__icontains=query) | bookings.filter(guest_email__icontains=query)

    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'query': query,
        'status_choices': Booking.Status.choices,
    }
    return render(request, 'dashboard/bookings.html', context)

@login_required
@booking_staff_required
def dashboard_booking_detail_view(request, reference_code):
    booking = get_object_or_404(Booking, reference_code=reference_code)
    staff_users = User.objects.filter(role__in=['BOOKING_STAFF', 'SUPER_ADMIN'], is_active=True)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            new_status = request.POST.get('status')
            note = request.POST.get('note', '').strip()
            quoted_price = request.POST.get('total_quoted_price')

            if quoted_price:
                try:
                    booking.total_quoted_price = float(quoted_price)
                except ValueError:
                    pass

            if new_status in dict(Booking.Status.choices):
                booking.transition_to(new_status, user=request.user, note=note)

                # Send notification to customer if linked
                if booking.customer:
                    Notification.objects.create(
                        user=booking.customer,
                        title=f"Booking Status Updated: {booking.get_status_display()}",
                        message=f"Your booking {booking.reference_code} status has been updated to '{booking.get_status_display()}'.",
                        link=f"/bookings/{booking.reference_code}/"
                    )

                messages.success(request, f"Booking status updated to {new_status}.")
            return redirect('dashboard:booking_detail', reference_code=booking.reference_code)

        elif action == 'assign_staff':
            staff_id = request.POST.get('staff_id')
            if staff_id:
                staff_user = User.objects.filter(id=staff_id).first()
                booking.assigned_staff = staff_user
                booking.save()
                messages.success(request, f"Booking assigned to {staff_user.get_full_name() or staff_user.username}.")
            else:
                booking.assigned_staff = None
                booking.save()
                messages.info(request, "Staff assignment cleared.")
            return redirect('dashboard:booking_detail', reference_code=booking.reference_code)

        elif action == 'update_notes':
            booking.internal_notes = request.POST.get('internal_notes', '').strip()
            booking.save()
            messages.success(request, "Internal staff notes updated.")
            return redirect('dashboard:booking_detail', reference_code=booking.reference_code)

    history = booking.status_history.all()
    payments = booking.payment_records.all()

    context = {
        'booking': booking,
        'staff_users': staff_users,
        'history': history,
        'payments': payments,
        'status_choices': Booking.Status.choices,
    }
    return render(request, 'dashboard/booking_detail.html', context)

@login_required
@content_manager_required
def dashboard_packages_view(request):
    packages = TravelPackage.objects.select_related('destination').all()
    return render(request, 'dashboard/packages.html', {'packages': packages})

@login_required
@content_manager_required
def dashboard_package_create_view(request):
    destinations = Destination.objects.filter(is_published=True)
    if request.method == 'POST':
        title = request.POST.get('title')
        destination_id = request.POST.get('destination')
        overview = request.POST.get('overview')
        duration_days = request.POST.get('duration_days', 5)
        duration_nights = request.POST.get('duration_nights', 4)
        price_per_person = request.POST.get('price_per_person')
        inclusions = request.POST.get('inclusions')
        exclusions = request.POST.get('exclusions')
        travel_requirements = request.POST.get('travel_requirements')
        cover_image = request.FILES.get('cover_image')
        is_featured = request.POST.get('is_featured') == 'on'
        status = request.POST.get('status', 'DRAFT')

        destination = get_object_or_404(Destination, id=destination_id)

        package = TravelPackage.objects.create(
            destination=destination,
            title=title,
            overview=overview,
            duration_days=int(duration_days),
            duration_nights=int(duration_nights),
            price_per_person=float(price_per_person),
            inclusions=inclusions,
            exclusions=exclusions,
            travel_requirements=travel_requirements,
            cover_image=cover_image,
            is_featured=is_featured,
            status=status,
            created_by=request.user
        )

        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='TravelPackage',
            object_id=str(package.id),
            details=f"Created package: {package.title}"
        )

        messages.success(request, f"Travel Package '{package.title}' created successfully!")
        return redirect('dashboard:packages')

    return render(request, 'dashboard/package_form.html', {'destinations': destinations})

@login_required
@booking_staff_required
def dashboard_enquiries_view(request):
    enquiries = CustomEnquiry.objects.all()
    return render(request, 'dashboard/enquiries.html', {'enquiries': enquiries})

@login_required
@booking_staff_required
def dashboard_enquiry_detail_view(request, pk):
    enquiry = get_object_or_404(CustomEnquiry, pk=pk)
    staff_users = User.objects.filter(role__in=['BOOKING_STAFF', 'SUPER_ADMIN'], is_active=True)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            enquiry.status = request.POST.get('status')
            enquiry.internal_notes = request.POST.get('internal_notes', '').strip()
            enquiry.save()
            messages.success(request, f"Enquiry status updated to {enquiry.get_status_display()}.")
        elif action == 'add_log':
            channel = request.POST.get('channel')
            msg = request.POST.get('message')
            if msg:
                EnquiryCommunicationLog.objects.create(
                    enquiry=enquiry,
                    staff=request.user,
                    channel=channel,
                    message=msg
                )
                messages.success(request, "Communication log recorded.")
        return redirect('dashboard:enquiry_detail', pk=enquiry.pk)

    logs = enquiry.communication_logs.all()

    context = {
        'enquiry': enquiry,
        'logs': logs,
        'staff_users': staff_users,
        'status_choices': CustomEnquiry.Status.choices,
    }
    return render(request, 'dashboard/enquiry_detail.html', context)

@login_required
@booking_staff_required
def dashboard_payments_view(request):
    payments = PaymentRecord.objects.select_related('booking', 'verified_by').all()

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        new_status = request.POST.get('payment_status')
        payment = get_object_or_404(PaymentRecord, pk=payment_id)
        payment.payment_status = new_status
        payment.verified_by = request.user
        payment.save()

        # Check if booking can be updated to AWAITING_PAYMENT or CONFIRMED
        if new_status == PaymentRecord.Status.VERIFIED:
            if payment.booking.is_fully_paid or payment.booking.status in ['UNDER_REVIEW', 'AWAITING_PAYMENT', 'QUOTED']:
                payment.booking.transition_to(
                    Booking.Status.CONFIRMED,
                    user=request.user,
                    note=f"Payment of ${payment.amount} verified by {request.user.username}."
                )

        messages.success(request, f"Payment status for ref {payment.payment_reference} updated to {new_status}.")
        return redirect('dashboard:payments')

    return render(request, 'dashboard/payments.html', {'payments': payments})

@login_required
@admin_required
def dashboard_users_view(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        target_user = get_object_or_404(User, id=user_id)
        if new_role in dict(User.Role.choices):
            target_user.role = new_role
            if new_role == User.Role.SUPER_ADMIN:
                target_user.is_staff = True
            target_user.save()
            messages.success(request, f"Role for user '{target_user.username}' updated to {target_user.get_role_display()}.")
        return redirect('dashboard:users')

    return render(request, 'dashboard/users.html', {'users': users, 'role_choices': User.Role.choices})

@login_required
@admin_required
def dashboard_settings_view(request):
    settings_obj = SiteSettings.load()
    if request.method == 'POST':
        settings_obj.site_name = request.POST.get('site_name', settings_obj.site_name)
        settings_obj.tagline = request.POST.get('tagline', settings_obj.tagline)
        settings_obj.contact_email = request.POST.get('contact_email', settings_obj.contact_email)
        settings_obj.contact_phone = request.POST.get('contact_phone', settings_obj.contact_phone)
        settings_obj.whatsapp_number = request.POST.get('whatsapp_number', settings_obj.whatsapp_number)
        settings_obj.office_address = request.POST.get('office_address', settings_obj.office_address)
        settings_obj.currency_code = request.POST.get('currency_code', settings_obj.currency_code)
        settings_obj.currency_symbol = request.POST.get('currency_symbol', settings_obj.currency_symbol)
        settings_obj.about_text = request.POST.get('about_text', settings_obj.about_text)
        settings_obj.save()

        messages.success(request, "Site configuration settings updated successfully.")
        return redirect('dashboard:settings')

    return render(request, 'dashboard/settings.html', {'settings': settings_obj})
