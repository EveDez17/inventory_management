from django.db import models

from django.utils import timezone

from django.conf import settings

from dateutil.relativedelta import relativedelta


class Address(models.Model):
    street_number = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    post_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_number} {self.street_name}, {self.city}, {self.county}, {self.country}, {self.post_code}"


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    supplier_contact = models.CharField(max_length=255)
    supplier_email = models.EmailField()
    supplier_contact_number = models.CharField(max_length=20)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "suppliers"

    def __str__(self):
        return self.supplier_name


# Custom manager to filter out soft-deleted SKUs
class ActiveSKUManager(models.Manager):
    def get_queryset(self):
        # Return only instances where is_deleted is False
        return super().get_queryset().filter(is_deleted=False)


# SKU model for stock keeping units with soft deletion support
class SKU(models.Model):
    sku_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=255)
    bbe = models.DateField(verbose_name="Best Before End")
    batch = models.CharField(max_length=255)
    manufacturing_date = models.DateField()
    shelf_life_end = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)  # Flag for soft deletion
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp of deletion
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="skus"
    )

    # Default and custom managers
    objects = models.Manager()
    active_objects = ActiveSKUManager()

    def save(self, *args, **kwargs):
        # Automatically calculate shelf_life_end based on manufacturing_date if not set
        if not self.shelf_life_end and self.manufacturing_date:
            self.shelf_life_end = self.manufacturing_date + relativedelta(months=24)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Implement soft delete by setting is_deleted flag and deleted_at timestamp
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Restore a soft-deleted SKU
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name


# Inventory model to track SKU quantities and ownership
class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    sku = models.ForeignKey(
        SKU, on_delete=models.SET_NULL, null=True, related_name="inventory_entries"
    )
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.sku.name} - {self.user.username}"


# Category model for categorizing SKUs
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
