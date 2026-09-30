from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('instructions/<str:reference_code>/', views.payment_instructions_view, name='instructions'),
]
