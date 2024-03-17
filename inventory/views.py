from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from .forms import UserRegisterForm, CategoryForm
from .models import Inventory, Category  # Assuming you have a Category model
from django.conf import settings  # Import Django settings
from .models import SKU, Category
from django.db.models import Q
from django.core.paginator import Paginator

# Index view, showing the homepage
class Index(TemplateView):
    template_name = 'inventory/index.html'



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


