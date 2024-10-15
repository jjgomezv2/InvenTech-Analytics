from django.shortcuts import render
from inventech.models import Product, ProductUnit
from account.models import UserProfile

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def graphics(request):

    user = request.user
    user_profile = UserProfile.objects.get(user=user) # Our user
    is_manager = user.groups.filter(name='Managers').exists()

    matplotlib.use('Agg')

    # Obtain all products

    products = Product.objects.filter(assigned_company = user_profile.company_idCompany)

    # Dictionary

    product_counts_by_sales = {}

    # Filtrate

    for product in products:

        name = product.product_name
        product_counts_by_sales[name] = product.product_sales

    bar_width = 0.5

    bar_positions = range(len(product_counts_by_sales))

    product_counts_by_expiration = {}

    for product in products:
        
        expiredUnits = ProductUnit.verifyExpiration(product)
        product.product_expiration_count = len(expiredUnits)
        product.save()

        name = product.product_name
        product_counts_by_expiration[name] = product.product_expiration_count

    plt.bar(bar_positions, product_counts_by_sales.values(), width=bar_width, align='center')

    plt.title('Sales per product')
    plt.xlabel('Name')
    plt.ylabel('Sales')
    plt.xticks(bar_positions, product_counts_by_sales.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Graphic 2

    plt.bar(bar_positions, product_counts_by_expiration.values(), width=bar_width, align='center')

    plt.title('Expiration per product')
    plt.xlabel('Name')
    plt.ylabel('Expiration count')
    plt.xticks(bar_positions, product_counts_by_expiration.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png)
    graphic2 = graphic2.decode('utf-8')

    return render(request, 'graphics.html', {'graphic':graphic,'graphic2': graphic2, 'is_manager': is_manager})

    
