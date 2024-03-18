from django.urls import path
from .views import Index, SignUpView, InventoryDashboardView, search_skus, InventorySearchResultsView, SKUDetailView,  AddSKUView, sku_added_success_view, DeleteSKUView, sku_delete_list_view, perform_sku_deletion, EditSKUView, sku_list_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    
    path('dashboard/', InventoryDashboardView.as_view(), name='inventory_dashboard'),
    
    path('search/', InventorySearchResultsView.as_view(), name='inventory_search_results'),
    
    path('sku/<int:pk>/', SKUDetailView.as_view(), name='sku_details'),
    
    path('add_sku/', AddSKUView.as_view(), name='add_sku'),
    
    path('success/', sku_added_success_view, name='success_url_name'),

    # Path for confirming the deletion of a single SKU
    path('sku/delete/<int:pk>/', DeleteSKUView.as_view(), name='delete_sku'),

    # Path for listing SKUs for bulk deletion
    path('delete-skus/', sku_delete_list_view, name='delete_sku_list'),

    # Path for performing the bulk deletion
    path('delete-skus/perform/', perform_sku_deletion, name='perform_sku_deletion'),
    
    path('skus/', sku_list_view, name='sku_list'),
   
    path('sku/edit/<int:pk>/', EditSKUView.as_view(), name='edit_sku'),
    
    path('search_skus/', search_skus, name='search_skus'),
    
    path('signup/', SignUpView.as_view(), name='signup'),  
    
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'), 
    
]


