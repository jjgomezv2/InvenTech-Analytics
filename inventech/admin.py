from django.contrib import admin
from .models import Product, ProductUnit

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductUnit)