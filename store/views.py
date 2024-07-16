from django.shortcuts import render, get_object_or_404
from .models import Store

# Create your views here.

def store_profile(request, slug):
    store = get_object_or_404(Store, slug=slug)
    categories = store.category.all()

    return render(request, 'store/profile.html', {
        'store': store,
        'categories': categories
    })