# Generated by Django 5.0.7 on 2024-10-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventech', '0008_product_product_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_expiration_count',
            field=models.IntegerField(default=0),
        ),
    ]
