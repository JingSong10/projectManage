from django.urls import path

from app01 import views

urlpatterns = [
    path('register/', views.register),
    path('index/', views.getredisinfo)
]