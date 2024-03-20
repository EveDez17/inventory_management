from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_warehouse_security = models.BooleanField("Is warehouse security", default=False)
    is_warehouse_receptionist = models.BooleanField(
        "Is warehouse receptionist", default=False
    )
    is_warehouse_operative = models.BooleanField(
        "Is warehouse operative", default=False
    )
    is_inventory_admin = models.BooleanField("Is inventory admin", default=False)
    is_warehouse_admin = models.BooleanField("Is warehouse admin", default=False)
    is_inventory_teamleader = models.BooleanField(
        "Is inventory teamleader", default=False
    )
    is_warehouse_teamleader = models.BooleanField(
        "Is warehouseteamleader", default=False
    )
    is_inventory_manager = models.BooleanField("Is inventory manager", default=False)
    is_warehouse_manager = models.BooleanField("Is warehouse manager", default=False)
    is_warehouse_operational_manager = models.BooleanField(
        "Is warehouse operationalmanager", default=False
    )
