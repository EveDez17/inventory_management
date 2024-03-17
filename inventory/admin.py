from django.contrib import admin
from .models import SKU, Inventory, Category

# Register your models here
admin.site.register(SKU)
admin.site.register(Inventory)
admin.site.register(Category)

