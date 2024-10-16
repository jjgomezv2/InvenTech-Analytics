from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, ProductUnit
from .suggestions import Handling_suggestions, Price_suggestions

from account.models import UserProfile

import openai
from openai import RateLimitError

import markdown
 
from .forms import ProductForm, UnitForm

from django.db.models import F

from django.db.models import F

from django.core.exceptions import ObjectDoesNotExist

@login_required
def delete_product(request, product_id):
    # Obtener el producto por su ID
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        # Eliminar todas las unidades relacionadas con el producto
        ProductUnit.objects.filter(product_id_foreign=product).delete()

        # Después de eliminar las unidades, eliminar el producto
        product.delete()

        # Redirigir a la página principal después de la eliminación
        return redirect('home')

    # Manejar solicitudes GET o métodos no permitidos
    return HttpResponse("Invalid request method.", status=405)

@login_required
def delete_units(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        units_to_delete = int(request.POST.get('units_to_delete', 0))
        
        
        units = ProductUnit.objects.filter(product_id_foreign=product).order_by('unit_expirationDate')  

        units_deleted = 0
        for unit in units:
            if units_deleted < units_to_delete:
                unit.delete()
                units_deleted += 1
            else:
                break

        product.product_stock = F('product_stock') - units_deleted
        product.save(update_fields=['product_stock'])

        return redirect('home')

    return HttpResponse("Invalid request method.", status=405)

@login_required
def create_product(request):
    user = request.user

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.assigned_company = user.company_idCompany
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'productCreation.html', {'form': form})

@login_required
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
        
        return suggestion
    
    except RateLimitError as e:
        print(f"RateLimitError: {e}")
        return "API quota exceeded. Please try again later."
    except Exception as e:
        print(f"Error fetching suggestion: {e}")
        return "An error occurred while fetching suggestion."

# Create your views here.
@login_required
def home(request):
    user = request.user  # Django's user

    if user.is_authenticated:

        user_profile = UserProfile.objects.get(user=user) # Our user

        searchTerm = request.GET.get('searchProduct')
        low_quantity_products=Product.verifyLowQuantity(user=user_profile)

        if searchTerm:
            products = Product.objects.filter(product_name__icontains = searchTerm, assigned_company = user_profile.company_idCompany)
        else:
            products = Product.objects.filter(assigned_company = user_profile.company_idCompany)

    else:
        products = []
        low_quantity_products = []
        searchTerm = None
        
    
    for unit in ProductUnit.objects.all():
        unit.save()
        
    for product in products:
        if product.product_price == 0:
            product.product_price = suggest_price(product)
            product.save()
        if product.product_assigned_suggestions == "Blank":
            product.product_assigned_suggestions = assign_suggestions(product)
            product.save()
            
    
    is_manager = user.groups.filter(name='Managers').exists()
    
    return render(request, 'home.html', {'searchTerm':searchTerm, 'products': products, 'low_quantity_products': low_quantity_products, 'is_manager': is_manager})

@login_required
def unitsDetail(request, product_id):
    searchTerm = request.GET.get('searchUnit')
    if searchTerm:
        units = ProductUnit.objects.filter(unit_id__icontains = searchTerm)
    else:
        units = ProductUnit.objects.all()
        
    product = get_object_or_404(Product, product_id=product_id)
    expiredUnits = ProductUnit.verifyExpiration(product)
    
    return render(request, 'unitsDetail.html', {'searchTerm':searchTerm, 'product': product, 'units': units, 'expiredUnits': expiredUnits})