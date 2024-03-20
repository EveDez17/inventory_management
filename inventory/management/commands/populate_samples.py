from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Address, Supplier, SKU, Inventory, Category
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **options):
        # Populate Categories
        categories = ["Ambient Foods", "Chilled Foods", "Frozen Foods"]
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Successfully populated categories"))

        # Populate Address
        address = Address.objects.create(
            street_number="123",
            street_name="Main Street",
            city="Anytown",
            county="Anystate",
            country="Country",
            post_code="12345",
        )

        # Populate Supplier
        supplier = Supplier.objects.create(
            supplier_name="Example Supplier",
            supplier_contact="John Doe",
            supplier_email="john.doe@example.com",
            supplier_contact_number="1234567890",
            address=address,
        )

        # Check for a user or create a new one for the inventory sample
        user, _ = User.objects.get_or_create(
            username="sampleuser", defaults={"email": "sample@example.com"}
        )
        user.set_password("samplepass")
        user.save()

        # Populate Category
        category, _ = Category.objects.get_or_create(name="Example Category")

        # Populate SKU
        sku = SKU.objects.create(
            name="Sample Product",
            description="This is a sample product.",
            category=category,  # Make sure this is a ForeignKey relation
            weight=1.00,
            dimensions="10x10x10",
            bbe=timezone.now() + relativedelta(months=6),
            batch="BATCH001",
            manufacturing_date=timezone.now(),
            supplier=supplier,
        )

        # Populate Inventory
        inventory = Inventory.objects.create(
            sku=sku,
            category=category,  # Make sure this is a ForeignKey relation
            user=user,
            quantity=100,
        )

        self.stdout.write(self.style.SUCCESS("Successfully populated all sample data"))
