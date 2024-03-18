from django.contrib import admin
from django.utils.html import format_html
from .models import SKU, Inventory, Category, Address, Supplier

@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    # Replacing 'supplier' with 'get_supplier_name' in list_display
    list_display = ('sku_id', 'name', 'category', 'bbe', 'is_deleted', 'get_supplier_name')
    list_filter = ('is_deleted', 'category', 'supplier')
    search_fields = ('name', 'sku_id', 'batch')

    actions = ['restore_sku']

    def restore_sku(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
    restore_sku.short_description = "Restore selected SKUs"

    def get_supplier_name(self, obj):
        # Checking if the SKU has a supplier before trying to access its name
        return obj.supplier.supplier_name if obj.supplier else "No Supplier"
    get_supplier_name.short_description = 'Supplier Name'
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(supplier__supplier_name__icontains=search_term)
            use_distinct = True  # Use distinct if searching across relationships to avoid duplicates
        return queryset, use_distinct


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'sku', 'user', 'quantity', 'date_created')
    list_filter = ('user',)
    search_fields = ('sku__name', 'user__username')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'supplier_email', 'supplier_contact_number', 'address', 'list_skus')
    list_filter = ('supplier_name',)
    search_fields = ('supplier_name', 'supplier_email')

    def list_skus(self, obj):
        # Accesses the related SKUs using the 'skus' related_name set in the ForeignKey relationship in the SKU model
        skus = obj.skus.all()
        # Joins the SKU names (or any identifier you prefer) into a comma-separated list
        sku_list = ", ".join([sku.name for sku in skus])
        # Returns the list of SKUs for display, or "No SKUs" if the list is empty
        return format_html("<span>{}</span>", sku_list) if sku_list else "No SKUs"
        
    list_skus.short_description = "SKUs"  # Sets a header for the column in the admin list view
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_number', 'street_name', 'city', 'county', 'country', 'post_code')
    list_filter = ('country', 'county', 'city')  # Allows filtering by these fields in the admin
    search_fields = ('street_name', 'city', 'post_code', 'county', 'country')  # Enables a search box for these fields

    # Optional: Customize the form layout in the admin detail view
    fieldsets = (
        (None, {
            'fields': ('street_number', 'street_name', 'city', 'county')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('country', 'post_code'),
        }),
    )




