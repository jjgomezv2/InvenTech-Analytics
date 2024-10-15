from django.urls import path
from . import views

# Urls of Data Analytics
urlpatterns = [
    path('graphics/', views.graphics, name ='graphics'),
    path('logout/', views.graphics, name='logoutaccount'),
]