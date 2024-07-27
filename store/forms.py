from typing import Any
from django import forms

from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image','status','options')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)