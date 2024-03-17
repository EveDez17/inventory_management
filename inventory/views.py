from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.views.generic import TemplateView, View

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LogoutView

from .forms import UserRegisterForm

from .models import Inventory, SKU, Supplier

from django.http import JsonResponse

# Index view, showing the homepage
class Index(TemplateView):
    template_name = 'inventory/index.html'
    
class InventoryDashboardView(TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get search query from request
        search_query = self.request.GET.get('search_query', '')

        # Filter inventory_list based on the search query
        if search_query:
            context['inventory_list'] = Inventory.objects.filter(
                sku__name__icontains=search_query
            )
        else:
            context['inventory_list'] = Inventory.objects.all()

        context['sku_count'] = SKU.active_objects.count()
        context['supplier_count'] = Supplier.objects.count()
        context['search_query'] = search_query  # Pass search_query to the template to reuse it in the search form
        
        return context
    
def search_skus(request):
    query = request.GET.get('query', '')
    skus = SKU.objects.filter(name__icontains=query).values('name')[:5]  # Limit results to 5 for example
    return JsonResponse(list(skus), safe=False)



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


