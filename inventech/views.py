from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, ProductUnit

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchLocation')
    products = Product.objects.all()
    if searchTerm:
        units = ProductUnit.objects.filter(unit_location = searchTerm)
    else:
        units = ProductUnit.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'units': units, 'products': products})
    #return render(request, 'home.html')