from django.contrib import admin
from .models import SKU, Inventory, Category, Address, Supplier

@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('sku_id', 'name', 'category', 'bbe', 'is_deleted')
    list_filter = ('is_deleted', 'category',)
    search_fields = ('name', 'sku_id', 'batch')
    actions = ['restore_sku']

    def restore_sku(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
    restore_sku.short_description = "Restore selected SKUs"

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'sku', 'user', 'quantity', 'date_created')
    list_filter = ('user',)
    search_fields = ('sku__name', 'user__username')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_number', 'street_name', 'city', 'county', 'country', 'post_code')
    search_fields = ('city', 'street_name', 'post_code')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'supplier_email', 'supplier_contact_number', 'address', 'sku')
    list_filter = ('supplier_name',)
    search_fields = ('supplier_name', 'supplier_email', 'sku')


