from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Store, Product, Category

class UserForm(UserCreationForm): 
    # 繼承 UserCreationForm
    email = forms.EmailField(required=True, label='Email:')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()

        return user
    
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'slug', 'phone', 'address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image','status','options')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)