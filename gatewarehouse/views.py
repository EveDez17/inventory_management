# gatewarehouse/views.py

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

from django.views import View

from .models import VehicleLog

class GateWarehouseIndexView(TemplateView):
    template_name = 'gatewarehouse/gatewarehouse_index.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "gatewarehouse/gatehouse_dashboard.html"
    


