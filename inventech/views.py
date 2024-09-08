from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, ProductUnit
from .suggestions import Handling_suggestions, Price_suggestions

import openai
from openai import RateLimitError

import markdown
 
from .forms import ProductForm, UnitForm

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'productCreation.html', {'form': form})

def create_unit(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.product_id_foreign = product
            form.save()
            return redirect('home')
    else:
        form = UnitForm()
        

    return render(request, 'UnitCreation.html', {'form': form, 'product': product})
 
def assign_suggestions(product):

    try:
        hs = Handling_suggestions()
        suggestions = hs.get_suggestions(
            product.product_name,
            product.product_category,
            product.product_description
        )

        assigned_suggestions = markdown.markdown(suggestions)

        #print(assigned_suggestions)
        return assigned_suggestions
    
    except RateLimitError as e:
        print(f"RateLimitError: {e}")
        return "API quota exceeded. Please try again later."
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return "An error occurred while fetching suggestions."

def suggest_price(product):
    try:
        ps = Price_suggestions()
        suggestion = ps.get_price(
            product.product_name,
            product.product_category,
            product.product_description
            )
        
        suggestion = int(suggestion)
        
        #print(suggestion)
        return suggestion
    
    except RateLimitError as e:
        print(f"RateLimitError: {e}")
        return "API quota exceeded. Please try again later."
    except Exception as e:
        print(f"Error fetching suggestion: {e}")
        return "An error occurred while fetching suggestion."

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
        if product.product_price == 0:
            product.product_price = suggest_price(product)
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