# Generated by Django 5.0.3 on 2024-03-17 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('sku_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=255)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dimensions', models.CharField(max_length=255)),
                ('bbe', models.DateField(verbose_name='Best Before End')),
                ('batch', models.CharField(max_length=255)),
                ('manufacturing_date', models.DateField()),
                ('shelf_life_end', models.DateField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to=settings.AUTH_USER_MODEL)),
                ('sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_entries', to='inventory.sku')),
            ],
        ),
    ]