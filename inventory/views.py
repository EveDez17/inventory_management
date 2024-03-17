from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.views.generic import TemplateView, View

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LogoutView

from .forms import UserRegisterForm

from .models import Inventory, SKU, Supplier

# Index view, showing the homepage
class Index(TemplateView):
    template_name = 'inventory/index.html'
    
class InventoryDashboardView(TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_list'] = Inventory.objects.all()
        context['sku_count'] = SKU.active_objects.count()
        context['supplier_count'] = Supplier.objects.count()
        # Add more context data as needed for your dashboard
        return context



# Sign-up view, handling both GET and POST requests for user registration
class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form': form})

# Custom logout view, utilizing Django's built-in LogoutView
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')  # Redirect to index page after logout


