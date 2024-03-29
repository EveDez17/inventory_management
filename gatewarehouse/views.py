# gatewarehouse/views.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "gatewarehouse/gatehouse_dashboard.html"
