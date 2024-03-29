# gatewarehouse/urls.py

from django.urls import path
# Import Index from the inventory app's views, not the current app's views
from inventory.views import Index
from .views import DashboardView  # Import DashboardView from the current app

app_name = 'gatewarehouse'

urlpatterns = [
    # Use the Index view from the inventory app for the root URL of 'gatewarehouse'
    path('', Index.as_view(), name='index'),  
    # The DashboardView for 'dashboard/' URL within 'gatewarehouse'
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
]

