from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('auth/', include('apps.accounts.urls', namespace='accounts')),
    path('destinations/', include('apps.destinations.urls', namespace='destinations')),
    path('packages/', include('apps.packages.urls', namespace='packages')),
    path('bookings/', include('apps.bookings.urls', namespace='bookings')),
    path('enquiries/', include('apps.enquiries.urls', namespace='enquiries')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('gallery/', include('apps.gallery.urls', namespace='gallery')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
