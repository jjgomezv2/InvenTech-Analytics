from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Shipment

from inventech.models import Product, ProductUnit

from account.models import UserProfile

from .forms import ShipmentForm

from django.db.models import F

from django.core.exceptions import ObjectDoesNotExist


def sell_units(product_id, quantity):
    product = get_object_or_404(Product, product_id=product_id)    
    
    units = ProductUnit.objects.filter(product_id_foreign=product).order_by('unit_expirationDate')  

    units_deleted = 0
    for unit in units:
        if units_deleted < quantity:
            unit.delete()
            units_deleted += 1
            product.product_sales += 1
        else:
            break

    product.product_stock = F('product_stock') - units_deleted
    product.save(update_fields=['product_stock', 'product_sales'])

        
@login_required
def create_shipment(request, product_id):
    user = request.user

    if request.method == 'POST':
        form = ShipmentForm(request.POST, request.FILES)
        if form.is_valid():
            shipment = form.save(commit=False)
            # shipment.assigned_company = user.company_idCompany
            sell_units(product_id=product_id, quantity=shipment.shipment_units_quantity)
            form.save()
            return redirect('home')
    else:
        form = ShipmentForm()

    return render(request, 'shipmentCreation.html', {'form': form})



""" def deleteAndStoreUnitForShipment(request):
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

    return HttpResponse("Invalid request method.", status=405) """