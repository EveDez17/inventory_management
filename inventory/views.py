from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryForm
from .models import Inventory, SKU
from smart_inventory.settings import LOW_QUANTITY
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from django.views.generic import TemplateView

class Index(TemplateView):
    template_name = 'inventory/index.html'
    
LOW_QUANTITY = 10  # Example threshold for low inventory

class sku_dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = Inventory.objects.filter(user=request.user).order_by('inventory_id')

        low_inventory = items.filter(quantity__lte=LOW_QUANTITY)

        if low_inventory.exists():
            item_count = low_inventory.count()
            messages.error(request, f'{item_count} {"items" if item_count > 1 else "item"} {"have" if item_count > 1 else "has"} low inventory')

        low_inventory_ids = low_inventory.values_list('inventory_id', flat=True)

        return render(request, 'inventory/sku_dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})

    
class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')  # Redirect to index page after logout

    def get(self, request, *args, **kwargs):
        """Handle logout by a GET request."""
        return self.post(request, *args, **kwargs)


