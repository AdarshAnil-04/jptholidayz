from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.destination_list_view, name='list'),
    path('<slug:slug>/', views.destination_detail_view, name='detail'),
]
