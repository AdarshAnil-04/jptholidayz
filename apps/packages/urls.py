from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.package_list_view, name='list'),
    path('<slug:slug>/', views.package_detail_view, name='detail'),
]
