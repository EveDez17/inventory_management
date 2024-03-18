# Generated by Django 5.0.3 on 2024-03-18 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_address_supplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='sku',
        ),
        migrations.AddField(
            model_name='sku',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='inventory.supplier'),
            preserve_default=False,
        ),
    ]
