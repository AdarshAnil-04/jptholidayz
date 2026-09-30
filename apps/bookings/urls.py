from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('package/<slug:package_slug>/', views.create_booking_view, name='create'),
    path('success/<str:reference_code>/', views.booking_success_view, name='success'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('<str:reference_code>/', views.booking_detail_view, name='detail'),
]
