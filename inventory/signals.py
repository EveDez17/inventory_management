from django.apps import apps

from django.db.models.signals import post_migrate

from django.dispatch import receiver



@receiver(post_migrate)
def populate_predefined_categories(sender, **kwargs):
    # Check if the sender is the inventory app
    if sender.name == 'inventory':
        from .models import Category  # Import here to avoid circular import issues
        
        print("Post migrate signal for inventory app caught.")
        
        PREDEFINED_CATEGORIES = ['Ambient Foods', 'Chilled Foods', 'Frozen Foods']
        
        if not Category.objects.exists():
            for category_name in PREDEFINED_CATEGORIES:
                Category.objects.create(name=category_name)
                print(f"Created category: {category_name}")

