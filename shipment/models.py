from django.db import models
import uuid # Importa las librerías para generar códigos únicos UUID
from datetime import datetime # Date time library
from account.models import Company

# Función para generar un codigo UUID en versión 4
def generate_uuid():
    return str(uuid.uuid4())

class ShippingCompany(models.Model):
    idShippingCompany = models.CharField(max_length=50, default=generate_uuid, editable=False)
    shipComp_name = models.CharField(max_length=45)
    shipComp_phone = models.CharField(max_length=45)
    shipComp_website = models.CharField(max_length=45)


class Shipment(models.Model):
    ShippingCompany_idShippingCompany = models.ForeignKey(ShippingCompany, on_delete=models.CASCADE)
    idShipment = models.CharField(max_length=50, default=generate_uuid, editable=False)
    shipmentDate = models.DateField()
    shipment_address = models.CharField(max_length=45)
    shipment_customer_name = models.CharField(max_length=45)
    shipment_customer_lastname = models.CharField(max_length=45)
    shipment_customer_phone = models.CharField(max_length=45)
    shipment_customer_id = models.CharField(max_length=45)
    shipment_units_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.idShipment