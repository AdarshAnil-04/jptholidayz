from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index_view, name='index'),
    path('bookings/', views.dashboard_bookings_view, name='bookings'),
    path('bookings/<str:reference_code>/', views.dashboard_booking_detail_view, name='booking_detail'),
    path('packages/', views.dashboard_packages_view, name='packages'),
    path('packages/new/', views.dashboard_package_create_view, name='package_create'),
    path('enquiries/', views.dashboard_enquiries_view, name='enquiries'),
    path('enquiries/<int:pk>/', views.dashboard_enquiry_detail_view, name='enquiry_detail'),
    path('payments/', views.dashboard_payments_view, name='payments'),
    path('users/', views.dashboard_users_view, name='users'),
    path('settings/', views.dashboard_settings_view, name='settings'),
]
