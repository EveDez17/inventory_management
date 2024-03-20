import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Address, Supplier, SKU, Inventory, Category
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = "Populates the database with an expanded set of sample data"

    def add_arguments(self, parser):
        # Optional argument to specify the number of samples to create
        parser.add_argument('samples', type=int, nargs='?', default=10)

    def handle(self, *args, **options):
        samples = options['samples']

        # Example Categories
        category_names = [
            "Ambient Foods", "Chilled Foods", "Frozen Foods", 
            "Beverages", "Snacks", "Confectionery", "Health Foods", 
            "Meat & Poultry", "Seafood", "Dairy"
        ]
        for name in category_names:
            Category.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS(f"Successfully populated {len(category_names)} categories"))

        # Populate Address and Supplier
        for i in range(1, samples + 1):
            address = Address.objects.create(
                street_number=str(random.randint(1, 999)),
                street_name=f"Random Street {i}",
                city="Sample City",
                county="Sample County",
                country="Sampleland",
                post_code=f"{random.randint(10000, 99999)}"
            )

            Supplier.objects.create(
                supplier_name=f"Supplier {i}",
                supplier_contact=f"Contact {i}",
                supplier_email=f"supplier{i}@example.com",
                supplier_contact_number=f"{random.randint(1000000000, 9999999999)}",
                address=address
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully populated {samples} addresses and suppliers"))

        # Ensure there's a user for sample inventory
        user, _ = User.objects.get_or_create(
            username="sampleuser", defaults={"email": "sample@example.com", "password": "samplepass"}
        )
        user.set_password("samplepass")
        user.save()

        # Populate SKUs and Inventory
        categories = Category.objects.all()
        for i in range(1, samples * 2 + 1):  # Double the number of SKUs compared to suppliers
            category = random.choice(categories)
            supplier = Supplier.objects.order_by('?').first()  # Random supplier
            sku = SKU.objects.create(
                name=f"Product {i}",
                description="Sample product description.",
                category=category,
                weight=random.uniform(0.5, 5.0),
                dimensions=f"{random.randint(1, 20)}x{random.randint(1, 20)}x{random.randint(1, 20)}",
                bbe=timezone.now() + relativedelta(months=+6),
                batch=f"BATCH{i:03}",
                manufacturing_date=timezone.now() - relativedelta(days=random.randint(1, 365)),
                supplier=supplier
            )

            Inventory.objects.create(
                sku=sku,
                category=category,
                user=user,
                quantity=random.randint(10, 500)
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully populated {samples * 2} SKUs and inventory items"))
