from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.contrib import messages

from django.views.generic import TemplateView, View, ListView, DetailView

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LogoutView

from .forms import UserRegisterForm, SKUForm 

from .models import Inventory, SKU, Supplier

from django.http import JsonResponse

from django.views.generic.edit import CreateView

from django.http import HttpResponse

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

class InventorySearchResultsView(ListView):
    model = Inventory
    template_name = 'inventory/search_results.html'
    context_object_name = 'inventory_list'

    def get_queryset(self):
        query = self.request.GET.get('search_query')
        return Inventory.objects.filter(sku__name__icontains=query)
    
class SKUDetailView(DetailView):
    model = SKU
    template_name = 'inventory/sku_detail.html'  # Template for displaying SKU details
    context_object_name = 'sku'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sku = context['sku']
        
        # Ensure that the supplier is fetched correctly
        if sku.supplier:
            print("Supplier Name:", sku.supplier.supplier_name)  # Use supplier_name instead of name
            # You can print other supplier attributes if needed
        
        return context
    
class AddSKUView(CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'inventory/add_sku.html'  # The template that contains the form
    success_url = reverse_lazy('success_url_name')  # Use the name of the success URL

    def form_valid(self, form):
        response = super().form_valid(form)  
        messages.success(self.request, 'SKU has been added successfully!')
        return response
    

def sku_added_success_view(request):
    return render(request, 'inventory/sku_success.html')

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


