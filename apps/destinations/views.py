from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Destination

def destination_list_view(request):
    query = request.GET.get('q', '').strip()
    destinations = Destination.objects.filter(is_published=True)

    if query:
        destinations = destinations.filter(name__icontains=query) | destinations.filter(country__icontains=query)

    paginator = Paginator(destinations, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'destinations': page_obj.object_list,
        'query': query,
    }
    return render(request, 'destinations/list.html', context)

def destination_detail_view(request, slug):
    destination = get_object_or_404(Destination, slug=slug, is_published=True)
    packages = destination.packages.filter(status='PUBLISHED')
    related_destinations = Destination.objects.filter(is_published=True).exclude(pk=destination.pk)[:3]

    context = {
        'destination': destination,
        'packages': packages,
        'related_destinations': related_destinations,
    }
    return render(request, 'destinations/detail.html', context)
