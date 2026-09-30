from django.urls import path
from . import views

app_name = 'enquiries'

urlpatterns = [
    path('custom/', views.custom_enquiry_view, name='custom'),
]
