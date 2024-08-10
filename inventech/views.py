from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, ProductUnit

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchLocation')
    products = Product.objects.all()
    low_quantity_products=Product.verifyLowQuantity()
    if searchTerm:
        units = ProductUnit.objects.filter(unit_id = searchTerm)
    else:
        units = ProductUnit.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'units': units, 'products': products, 'low_quantity_products': low_quantity_products})
    #return render(request, 'home.html')