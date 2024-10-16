from django.contrib import admin
from .models import Shipment, ShippingCompany

# Register your models here.
admin.site.register(Shipment)
admin.site.register(ShippingCompany)