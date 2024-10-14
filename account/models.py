from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=50)
    company_address = models.CharField(max_length=50)
    company_phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.company_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idUser = models.CharField(max_length=20)
    user_name = models.CharField(max_length=50)
    user_lastname = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15)
    company_idCompany = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_name} {self.user_lastname} - {self.idUser}"
    