# Generated by Django 5.0.3 on 2024-03-20 17:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_initial"),
        ("role_based_login_system", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_inventory_admin",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_inventory_manager",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_inventory_teamleader",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_admin",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_manager",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_operational_manager",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_operative",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_receptionist",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_security",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_warehouse_teamleader",
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("DEFAULT_USER", "Default User"),
                    ("SECURITY", "Security"),
                    ("RECEPTIONIST", "Receptionist"),
                    ("WAREHOUSE_OPERATIVE", "Warehouse Operative"),
                    ("WAREHOUSE_ADMIN", "Warehouse Admin"),
                    ("WAREHOUSE_TEAM_LEADER", "Warehouse Team Leader"),
                    ("WAREHOUSE_MANAGER", "Warehouse Manager"),
                    ("INVENTORY_ADMIN", "Inventory Admin"),
                    ("INVENTORY_TEAM_LEADER", "Inventory Team Leader"),
                    ("INVENTORY_MANAGER", "Inventory Manager"),
                    ("OPERATIONAL_MANAGER", "Operational Manager"),
                ],
                default="DEFAULT_USER",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("f_name", models.CharField(max_length=255)),
                ("s_name", models.CharField(max_length=255)),
                ("dob", models.DateField()),
                ("p_email", models.EmailField(max_length=254, unique=True)),
                ("contact_number", models.CharField(max_length=20)),
                ("position", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.address",
                    ),
                ),
            ],
            options={
                "db_table": "employee",
            },
        ),
    ]
