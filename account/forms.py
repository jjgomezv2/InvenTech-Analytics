from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'company_idCompany']
        labels = {
            'idUser': "Employee's identification",
            'user_name': "Employee's name",
            'user_lastname': "Employee's lastname",
            'user_email': "Employee's email",
            'user_phone': "Employee's phone",
        }