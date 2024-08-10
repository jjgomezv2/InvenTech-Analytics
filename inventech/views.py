from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductUnit

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchProduct')
    low_quantity_products=Product.verifyLowQuantity()
    if searchTerm:
        products = Product.objects.filter(product_name__icontains = searchTerm)
    else:
        products = Product.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'products': products, 'low_quantity_products': low_quantity_products})
    #return render(request, 'home.html')
    
def unitsDetail(request, product_id):
    searchTerm = request.GET.get('searchUnit')
    if searchTerm:
        units = ProductUnit.objects.filter(unit_id__icontains = searchTerm)
    else:
        units = ProductUnit.objects.all()
        
    product = get_object_or_404(Product, product_id=product_id)
    
    return render(request, 'unitsDetail.html', {'searchTerm':searchTerm, 'product': product, 'units': units})