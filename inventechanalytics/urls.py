"""
URL configuration for inventechanalytics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventech import views as inventechViews

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inventechViews.home, name='home'),
    path('UnitsDetail/<str:product_id>/', inventechViews.unitsDetail, name='UnitsDetail'),
    path('productCreation/', inventechViews.create_product, name='productCreation'),
    path('unitCreation/<str:product_id>/', inventechViews.create_unit, name='unitCreation'),
    path('delete-units/<str:product_id>/', inventechViews.delete_units, name='delete_units'),
    path('delete_product/<str:product_id>/', inventechViews.delete_product, name='delete_product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)