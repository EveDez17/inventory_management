from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta

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
    sku = models.ForeignKey(SKU, on_delete=models.SET_NULL, null=True, related_name='inventory_entries')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.sku.name} - {self.user.username}"

# Category model for categorizing SKUs
class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
