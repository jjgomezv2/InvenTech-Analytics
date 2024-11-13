from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        exclude = ['idShipment']
        labels = {
            'ShippingCompany_idShippingCompany': 'Shipping Company',
            'shipment_address': 'Shipment address',
            'shipment_customer_name': 'Shipment customer name',
            'shipment_customer_lastname': 'Shipment customer last name',
            'shipment_customer_phone': 'Shipment customer phone',
            'shipment_customer_id': 'Shipment customer id',
            'shipment_units_quantity': 'Shipment units quantity',
            'shipmentDate': 'Shipment Date',
        }
    shipmentDate = forms.DateField(
        label= 'Shipment date',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )