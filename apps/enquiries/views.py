from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomEnquiryForm

def custom_enquiry_view(request):
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': request.user.phone or '',
        }

    if request.method == 'POST':
        form = CustomEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            messages.success(request, "Your custom travel request has been submitted! Our travel specialists will curate a personalized itinerary and reach out shortly.")
            return render(request, 'enquiries/enquiry_success.html', {'enquiry': enquiry})
        else:
            messages.error(request, "Failed to submit enquiry. Please check your form details.")
    else:
        form = CustomEnquiryForm(initial=initial_data)

    return render(request, 'enquiries/custom_enquiry.html', {'form': form})
