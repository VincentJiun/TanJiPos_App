from django.urls import path

from . import  views

urlpatterns = [
    path('<slug:slug>/', views.store_profile, name='store_profile'),
]