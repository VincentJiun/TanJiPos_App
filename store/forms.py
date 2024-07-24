from typing import Any
from django import forms

from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'slug', 'description', 'price', 'image',)

    def __init__(self, *args, **kwargs):
        store = kwargs.pop('store', None)
        super().__init__(*args, **kwargs)
        if store:
            self.fields['category'].queryset = Category.objects.filter(store=store)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)