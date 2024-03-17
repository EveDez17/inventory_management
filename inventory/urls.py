from django.urls import path
from .views import Index, SignUpView, sku_dashboard, CustomLogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),  # SignUpView corrected to use as_view()
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
    path('sku_dashboard/', sku_dashboard.as_view(), name='sku_dashboard'),  # Correctly refer to sku_dashboard
]


