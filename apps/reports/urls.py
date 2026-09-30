from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('itinerary-pdf/<str:reference_code>/', views.download_itinerary_pdf_view, name='itinerary_pdf'),
]
