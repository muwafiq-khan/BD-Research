from django.urls import path
from . import views


# urls.py
# Add this to your playground/urls.py (create this file if it doesn't exist)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.field_search, name='field_search'),
]