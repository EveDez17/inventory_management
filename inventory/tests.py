from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from .models import SKU, Inventory, Category
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class SKUTests(TestCase):
    def setUp(self):
        # Create a Category
        self.category = Category.objects.create(name="Electronics")
        # Create a SKU
        self.sku = SKU.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            category="Electronics",
            weight=1.5,
            dimensions="15x10x1",
            bbe=timezone.now().date(),
            batch="L123",
            manufacturing_date=timezone.now().date() - relativedelta(months=12)
        )

    def test_sku_creation(self):
        self.assertIsInstance(self.sku, SKU)
        self.assertEqual(self.sku.name, "Laptop")
    
    def test_sku_shelf_life_end_calculation(self):
        expected_shelf_life_end = self.sku.manufacturing_date + relativedelta(months=24)
        self.assertEqual(self.sku.shelf_life_end, expected_shelf_life_end)

class InventoryTests(TestCase):
    def setUp(self):
        # Create a User
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Reuse the Category and SKU setup from SKUTests
        self.category = Category.objects.create(name="Electronics")
        self.sku = SKU.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            category="Electronics",
            weight=1.5,
            dimensions="15x10x1",
            bbe=timezone.now().date(),
            batch="L123",
            manufacturing_date=timezone.now().date() - relativedelta(months=12)
        )
        # Create an Inventory item
        self.inventory = Inventory.objects.create(
            sku=self.sku,
            user=self.user,
            quantity=10
        )

    def test_inventory_creation(self):
        self.assertIsInstance(self.inventory, Inventory)
        self.assertEqual(self.inventory.quantity, 10)
        self.assertEqual(self.inventory.user.username, 'testuser')

# Similar structure can be followed for Category model tests

