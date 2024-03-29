from django.shortcuts import render
from django.views.generic import TemplateView

# Index view, showing the homepage
class Index(TemplateView):
    template_name = "inventory/index.html"
    
class InventoryDashboardView(TemplateView):
    template_name = "gatewarehouse/access_log_dashboard.html"