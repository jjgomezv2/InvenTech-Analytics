# Generated by Django 5.0.7 on 2024-10-16 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0002_alter_shipment_shippingcompany_idshippingcompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='ShippingCompany_idShippingCompany',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.shippingcompany'),
        ),
    ]
