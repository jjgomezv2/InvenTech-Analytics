from django import forms
from .models import Product, ProductUnit

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['product_id', 'product_price', 'product_stock', 'product_assigned_suggestions', 'assigned_company', 'product_sales', 'product_expiration_count']
        labels = {
            'product_name': 'Product name',
            'product_category': 'Product category',
            'product_description': 'Product description',
            'product_image': 'Product image',
        }
        
class UnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        exclude = ['product_id_foreign', 'unit_id', 'unit_quality_state']
        labels = {
            'unit_expirationDate': 'Expiration date',
        }
    unit_expirationDate = forms.DateField(
        label= 'Expiration date',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )