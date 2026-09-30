from django.shortcuts import render, redirect
from django.contrib import messages
from apps.destinations.models import Destination
from apps.packages.models import TravelPackage
from apps.gallery.models import GalleryImage
from .forms import ContactForm
from .models import SiteSettings

def home_view(request):
    featured_destinations = Destination.objects.filter(is_published=True, is_featured=True)[:6]
    if not featured_destinations.exists():
        featured_destinations = Destination.objects.filter(is_published=True)[:6]

    featured_packages = TravelPackage.objects.filter(status='PUBLISHED', is_featured=True).select_related('destination')[:6]
    if not featured_packages.exists():
        featured_packages = TravelPackage.objects.filter(status='PUBLISHED').select_related('destination')[:6]

    gallery_images = GalleryImage.objects.filter(is_featured=True)[:8]
    if not gallery_images.exists():
        gallery_images = GalleryImage.objects.all()[:8]

    context = {
        'featured_destinations': featured_destinations,
        'featured_packages': featured_packages,
        'gallery_images': gallery_images,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    settings_obj = SiteSettings.load()
    return render(request, 'core/about.html', {'settings': settings_obj})

def contact_view(request):
    settings_obj = SiteSettings.load()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for contacting JPT Holidays! Our travel team will respond to your enquiry within 24 hours.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the errors in the contact form.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form, 'settings': settings_obj})

def search_view(request):
    query = request.GET.get('q', '').strip()
    destination_id = request.GET.get('destination', '')
    max_price = request.GET.get('max_price', '')

    packages = TravelPackage.objects.filter(status='PUBLISHED').select_related('destination')

    if query:
        packages = packages.filter(title__icontains=query) | packages.filter(overview__icontains=query)
    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    if max_price:
        try:
            packages = packages.filter(price_per_person__lte=float(max_price))
        except ValueError:
            pass

    destinations = Destination.objects.filter(is_published=True)

    context = {
        'packages': packages,
        'query': query,
        'destinations': destinations,
        'selected_destination': destination_id,
        'max_price': max_price,
    }
    return render(request, 'core/search_results.html', context)
