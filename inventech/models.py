from django.db import models
import uuid # Importa las librerías para generar códigos únicos UUID

# Función para generar un codigo UUID en versión 4
def generate_uuid():
    return str(uuid.uuid4())

# Create your models here.
class Product(models.Model):
    product_id = models.CharField(max_length=50, default=generate_uuid, editable=False)
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=60)
    product_price = models.IntegerField()
    product_stock = models.IntegerField(default=0, editable = False)
    product_description = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='inventech/images/', blank = True)
    
    # Para que en el admin no salga object(1) sino el nombre del producto
    def __str__(self):
        return self.product_name
    
class ProductUnit(models.Model):
    product_id_foreign = models.ForeignKey(Product, on_delete=models.CASCADE) # Referencia el producto del cual es unidad, on_delete cascade indica que si se elimina el producto, se eliminan todas las unidades hijas de este
    unit_id = models.CharField(max_length=50, default=generate_uuid, editable=False)
    unit_expirationDate = models.DateField()
    unit_location = models.CharField(max_length=50)
    unit_quality_state = models.CharField(max_length=50, default="Buen estado", editable = False) # Discutir, campo se llena automaticamente con que el producto entra en buen estado
    
    def __str__(self):
        return self.unit_id
    
    