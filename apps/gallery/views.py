from django.shortcuts import render
from .models import GalleryImage, GalleryCategory

def gallery_view(request):
    category_slug = request.GET.get('category', '')
    categories = GalleryCategory.objects.all()
    images = GalleryImage.objects.all()

    selected_category = None
    if category_slug:
        selected_category = categories.filter(slug=category_slug).first()
        if selected_category:
            images = images.filter(category=selected_category)

    context = {
        'categories': categories,
        'images': images,
        'selected_category': selected_category,
        'category_slug': category_slug,
    }
    return render(request, 'gallery/gallery.html', context)
