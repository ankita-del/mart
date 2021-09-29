from django.forms import ModelForm, fields
from .models import Business,Product

class BusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ['verified']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['is_available','status']        