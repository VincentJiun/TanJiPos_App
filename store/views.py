from django.shortcuts import render, redirect,get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Store, Product, Category
from .forms import ProductForm, CategoryForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            store = Store.objects.create(manager=user, name=user.username, slug=user.username)
            # slug = user.store.slug

            return redirect('store_profile')
        
    else:
        form = UserCreationForm()

    return render(request, 'store/signup.html', {
        'form': form
    })

def signin(request):
    form = AuthenticationForm()

    if request.method == "POST":
        return_form = AuthenticationForm(data=request.POST)
        # print(return_form)
        if return_form.is_valid():
            user = return_form.get_user()
            login(request, user)
            # slug = user.store.slug
            return redirect('store_profile')

    
    return render(request, 'store/signin.html', {
        'form': form,
    })

def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def store_profile(request):
    products = request.user.store.product.all()   #.exclude(status=Product.DELETED)

    return render(request, 'store/profile.html', {
        'products': products
    })

@login_required
def add_product(request):
    store = request.user.store

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, store=store)

        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()

            messages.success(request, '新增商品完成')

            return redirect('store_profile')
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {
        'title': '新增餐點',
        'btn_title': '新增',
        'form':form
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            category = form.save(commit=False)
            category.store = request.user.store
            category.save()

            return redirect('store_profile')
    else:
        form = CategoryForm()

    return render(request, 'store/add_category.html', {
        'form':form
    })

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(store=request.user.store).get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, '修改完成')

            return redirect('store_profile')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/add_product.html', {
        'title': '修改餐點',
        'btn_title': '修改',
        'product': product,
        'form':form
    })

@login_required
def delete_product(request, pk):
    product = Product.objects.filter(store=request.user.store).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, '商品已刪除')

    return redirect('store_profile')