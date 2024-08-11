from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductUnit

""" # Generación de texto

from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import tensorflow as tf

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = TFGPT2LMHeadModel.from_pretrained("gpt2")

def generate_text(product):
    prompt = f"Hola. Por favor, dime condiciones y recomendaciones de manejo durante el almacenamiento y manipulación en bodega de un alimento categorizado como {product.product_category} y con esta descripción {product.product_description}."

    input_ids = tokenizer.encode(prompt, return_tensors="tf")
    max_length = max(100, len(input_ids[0]) + 50)  # Incrementa el tamaño según sea necesario
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return response[len(prompt):] """
 

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchProduct')
    low_quantity_products=Product.verifyLowQuantity()
    if searchTerm:
        products = Product.objects.filter(product_name__icontains = searchTerm)
    else:
        products = Product.objects.all()
        
    """ for product in products:
        product.generated_suggestions = generate_text(product)
        product.save() """
    
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