from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductUnit
from .handling_suggestions import Handling_suggestions

import openai
from openai import RateLimitError

import markdown
 
def assign_suggestions(product):

    try:
        hs = Handling_suggestions()
        suggestions = hs.get_suggestions(
            product.product_name,
            product.product_category,
            product.product_description
        )

        assigned_suggestions = markdown.markdown(suggestions)

        print(assigned_suggestions)
        return assigned_suggestions
    
    except RateLimitError as e:
        # Log the error for debugging
        print(f"RateLimitError: {e}")
        # Return a fallback message or handle the error gracefully
        return "API quota exceeded. Please try again later."
    except Exception as e:
        # Handle any other exceptions
        print(f"Error fetching suggestions: {e}")
        return "An error occurred while fetching suggestions."

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