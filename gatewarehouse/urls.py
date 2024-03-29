from django.urls import path
from .views import GateWarehouseIndexView, DashboardView, VehicleLogView

app_name = 'gatewarehouse'

urlpatterns = [
    path('', GateWarehouseIndexView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    
    # ... other URL patterns for gatewarehouse
]

