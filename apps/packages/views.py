from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from apps.destinations.models import Destination
from .models import TravelPackage, ItineraryDay

def package_list_view(request):
    query = request.GET.get('q', '').strip()
    destination_id = request.GET.get('destination', '')
    duration = request.GET.get('duration', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', '-created_at')

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
    if duration:
        if duration == 'short': # 1-3 days
            packages = packages.filter(duration_days__lte=3)
        elif duration == 'medium': # 4-7 days
            packages = packages.filter(duration_days__gte=4, duration_days__lte=7)
        elif duration == 'long': # 8+ days
            packages = packages.filter(duration_days__gte=8)

    valid_sorts = ['price_per_person', '-price_per_person', 'duration_days', '-created_at']
    if sort_by in valid_sorts:
        packages = packages.order_by(sort_by)

    paginator = Paginator(packages, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    destinations = Destination.objects.filter(is_published=True)

    context = {
        'page_obj': page_obj,
        'packages': page_obj.object_list,
        'destinations': destinations,
        'query': query,
        'selected_destination': destination_id,
        'selected_duration': duration,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'packages/list.html', context)

def package_detail_view(request, slug):
    package = get_object_or_404(TravelPackage, slug=slug, status='PUBLISHED')
    itinerary_days = package.itinerary_days.all().order_by('day_number')
    gallery_images = package.gallery_images.all().order_by('order')
    related_packages = TravelPackage.objects.filter(
        destination=package.destination,
        status='PUBLISHED'
    ).exclude(pk=package.pk)[:3]

    context = {
        'package': package,
        'itinerary_days': itinerary_days,
        'gallery_images': gallery_images,
        'related_packages': related_packages,
    }
    return render(request, 'packages/detail.html', context)
