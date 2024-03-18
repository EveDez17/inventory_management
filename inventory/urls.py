from django.urls import path
from .views import Index, SignUpView, InventoryDashboardView, search_skus, InventorySearchResultsView, SKUDetailView,  AddSKUView, sku_added_success_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', InventoryDashboardView.as_view(), name='inventory_dashboard'),
    path('search/', InventorySearchResultsView.as_view(), name='inventory_search_results'),
    path('sku/<int:pk>/', SKUDetailView.as_view(), name='sku_details'),
    path('add_sku/', AddSKUView.as_view(), name='add_sku'),
    path('success/', sku_added_success_view, name='success_url_name'),
    path('search_skus/', search_skus, name='search_skus'),
    path('signup/', SignUpView.as_view(), name='signup'),  # SignUpView corrected to use as_view()
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'), 
    
]


