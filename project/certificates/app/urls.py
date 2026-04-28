from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('login/', views.login),
    path('add_certificate/', views.add_certificate, name='add_certificate'), 
    path('verify/', views.verify_certificate, name='verify'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout, name='logout'),
]