# Generated by Django 5.0.7 on 2024-08-08 20:51

import django.db.models.deletion
import inventech.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(default=inventech.models.generate_uuid, editable=False, max_length=50)),
                ('product_name', models.CharField(max_length=50)),
                ('product_category', models.CharField(max_length=60)),
                ('product_price', models.IntegerField()),
                ('product_stock', models.IntegerField()),
                ('product_description', models.CharField(max_length=100)),
                ('product_image', models.ImageField(blank=True, upload_to='inventech/images/')),
            ],
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_id', models.CharField(default=inventech.models.generate_uuid, editable=False, max_length=50)),
                ('unit_expirationDate', models.DateField()),
                ('unit_location', models.CharField(max_length=50)),
                ('unit_quality_state', models.CharField(default='Buen estado', editable='False', max_length=50)),
                ('product_id_foreign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventech.product')),
            ],
        ),
    ]
