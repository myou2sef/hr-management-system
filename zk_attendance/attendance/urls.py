from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch/', views.fetch_attendance, name='fetch_attendance'),
]
