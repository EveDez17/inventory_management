from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"

    def ready(self):
        import inventory.signals
