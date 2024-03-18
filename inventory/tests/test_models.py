from django.test import TestCase
from django.contrib.auth.models import User
from inventory.models import SKU, Supplier, Address, Inventory, Category
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class ModelTestCase(TestCase):
    def setUp(self):
        # Create necessary instances for testing
        self.address = Address.objects.create(street_number="123", street_name="Main St", city="Anytown", county="Anycountry", country="Country", post_code="12345")
        self.supplier = Supplier.objects.create(supplier_name="Test Supplier", supplier_contact="John Contact", supplier_email="supplier@example.com", supplier_contact_number="123456789", address=self.address)
        self.category = Category.objects.create(name="Electronics")
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        self.sku = SKU.objects.create(name="Test Product", description="Test Description", category="Test Category", weight=1.0, dimensions="10x10x10", bbe=timezone.now().date(), batch="Batch1", manufacturing_date=timezone.now().date(), supplier=self.supplier)
        
        self.inventory = Inventory.objects.create(sku=self.sku, category=self.category, user=self.user, quantity=100)

    def test_sku_fields(self):
        # Testing SKU fields and automatic shelf_life_end calculation
        self.assertEqual(self.sku.name, "Test Product")
        self.assertTrue(self.sku.shelf_life_end, self.sku.manufacturing_date + relativedelta(months=24))

    def test_sku_soft_delete(self):
        # Testing soft delete functionality
        self.assertFalse(self.sku.is_deleted)
        self.sku.delete()
        self.assertTrue(self.sku.is_deleted)
        self.assertIsNotNone(self.sku.deleted_at)
        # Testing restore functionality
        self.sku.restore()
        self.assertFalse(self.sku.is_deleted)
        self.assertIsNone(self.sku.deleted_at)

    def test_inventory_association(self):
        # Testing ForeignKey relationships
        self.assertEqual(self.inventory.sku, self.sku)
        self.assertEqual(self.inventory.user, self.user)
        self.assertEqual(self.inventory.category, self.category)

    def test_category_creation(self):
        # Testing Category creation
        self.assertEqual(self.category.name, "Electronics")
