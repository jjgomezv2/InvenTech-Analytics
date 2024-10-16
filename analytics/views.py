from django.shortcuts import render
from inventech.models import Product, ProductUnit
from account.models import UserProfile

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json
import markdown

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

    
def selling(request):

    user = request.user
    user_profile = UserProfile.objects.get(user=user) # Our user

    products = Product.objects.filter(assigned_company = user_profile.company_idCompany)

    _ = load_dotenv('openAI.env')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openAI_api_key'),
    )


    max_product = None
    max_expired = None

    if products:
        max_product = products[0]
        max_expired = products[0]

        for item in products:

            if item.product_expiration_count > max_expired.product_expiration_count:
                max_expired = item

            if item.product_sales > max_product.product_sales:
                max_product = item

    max_expired_name = ""
    max_product_name = ""

    if max_expired and max_expired.product_expiration_count == 0:
        max_expired = None
    else:
        max_expired_name = max_expired.product_name

    if max_product and max_product.product_sales == 0:
        max_product = None
    else:
        max_product_name = max_product.product_name


    not_saled_products = Product.objects.filter(product_sales = 0)

    not_saled_text = ""

    for item in not_saled_products:
        not_saled_text += f'{item.product_name}\n'


    prompt = f"""Objective:

    This system is designed to optimize inventory management for food companies by identifying trends in product sales and expiration, as well as providing actionable selling suggestions to reduce waste and increase profitability.

    Inputs Required:

    Most Sold Product: {max_product_name} (Ignore if None)
    Most Expired Product: {max_expired_name} (Ignore if None)
    Non-Sold Products:

    {not_saled_text} 

    (Ignore if None)

    Output:

    Based on the provided data, the system will generate personalized selling suggestions, which may include strategies such as product bundling, promotional discounts, or marketing campaigns targeted at improving sales performance and reducing product expiration rates. These suggestions are aimed at benefiting the company by increasing revenue, reducing waste, and improving overall inventory management.

    And to do the selling Suggestions:

    1. Promote the Most Sold Product:

    - Strategy: Increase focus on the most sold product by offering bundle deals or limited-time promotions. Consider cross-selling this product with slow-moving items or products approaching their expiration dates.
    - Benefit: This leverages the popularity of the best-selling product to boost sales of underperforming items, helping to clear inventory more efficiently.
    
    2. Address the Most Expired Product:

    - Strategy: Implement discounts or flash sales to move the most expired product before it spoils. Adjust inventory orders to better align with actual sales patterns, reducing overstock of this product in the future.
    - Benefit: Reduces waste by ensuring that products nearing their expiration are sold quickly, minimizing financial losses and helping maintain freshness in the inventory.
    
    3. Revitalize Non-Sold Products:

    - Strategy: Evaluate the reasons behind the lack of sales for certain products (e.g., poor visibility, low demand, pricing issues) and implement targeted marketing strategies, such as highlighting these items in promotional material, adjusting pricing, or offering special deals.
    - Benefit: Provides an opportunity to reintroduce these products to customers and potentially unlock new revenue streams. If certain items remain unsold, the system can suggest removing them from inventory to reduce holding costs."""


    model="gpt-4o-mini"

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature = 0,
        max_tokens = 1000,
    )

    sellingNotFormated = response.choices[0].message.content
    sellSug = markdown.markdown(sellingNotFormated)

    return render(request, 'selling.html', {'suggestions': sellSug})