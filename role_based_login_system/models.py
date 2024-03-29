from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from inventory.models import Address  

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Role(models.TextChoices):
        DEFAULT_USER = "DEFAULT_USER", 'Default User'
        SECURITY = "SECURITY", 'Security'
        RECEPTIONIST = "RECEPTIONIST", 'Receptionist'
        WAREHOUSE_OPERATIVE = "WAREHOUSE_OPERATIVE", 'Warehouse Operative'
        WAREHOUSE_ADMIN = "WAREHOUSE_ADMIN", 'Warehouse Admin'
        WAREHOUSE_TEAM_LEADER = "WAREHOUSE_TEAM_LEADER", 'Warehouse Team Leader'
        WAREHOUSE_MANAGER = "WAREHOUSE_MANAGER", 'Warehouse Manager'
        INVENTORY_ADMIN = "INVENTORY_ADMIN", 'Inventory Admin'
        INVENTORY_TEAM_LEADER = "INVENTORY_TEAM_LEADER", 'Inventory Team Leader'
        INVENTORY_MANAGER = "INVENTORY_MANAGER", 'Inventory Manager'
        OPERATIONAL_MANAGER = "OPERATIONAL_MANAGER", 'Operational Manager'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.DEFAULT_USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_role(self, role):
        return self.role == role
        
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    f_name = models.CharField(max_length=255)
    s_name = models.CharField(max_length=255)
    dob = models.DateField()
    p_email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    start_date = models.DateField()

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.f_name} {self.s_name}"
