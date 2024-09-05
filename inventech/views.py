from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductUnit
 
def assign_suggestions(product):
    suggestions = {
    'Lacteos': '• Mantener entre 4°C y 25°C. \n • Evitar temperaturas extremas. \n • Evitar la luz solar directa y fuentes de luz intensa. \n • Mantener la humedad relativa entre 50% y 70%. \n • Asegurar una buena ventilación en la bodega.',
    'Carnes frias': '• Mantén el producto entre 0°C y 4°C. \n • La humedad relativa del aire debe mantenerse entre 75% y 85%. \n • Si se requiere almacenamiento a largo plazo, la temperatura debe mantenerse a -18°C (0°F) o más baja',
    'Pollo': '• Mantener a -18°C (0°F) o menos. Es crucial que el pollo se mantenga congelado en todo momento. \n • Evitar fluctuaciones de temperatura que puedan causar descongelamiento parcial y recongelamiento. \n • Mantener una iluminación baja en el área de almacenamiento para evitar la degradación de la calidad del producto.'
    }
    
    for key in suggestions:
        if key == product.product_category:
            assigned_suggestions = suggestions.get(key)
            
    return assigned_suggestions

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchProduct')
    low_quantity_products=Product.verifyLowQuantity()
    if searchTerm:
        products = Product.objects.filter(product_name__icontains = searchTerm)
    else:
        products = Product.objects.all()
        
    
    for unit in ProductUnit.objects.all():
        unit.save()
        
    for product in products:
        product.assigned_suggestions = assign_suggestions(product)
        product.save()
    
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