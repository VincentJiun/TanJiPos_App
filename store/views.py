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

            return redirect('store_manage')
        
    else:
        form = UserCreationForm()

    return render(request, 'store/signup.html', {
        'form': form
    })

def signin(request):
    form = AuthenticationForm()

    if request.method == "POST":
        return_form = AuthenticationForm(data=request.POST)

        if return_form.is_valid():
            user = return_form.get_user()
            login(request, user)
            # slug = user.store.slug
            return redirect('store_manage')

    
    return render(request, 'store/signin.html', {
        'form': form,
    })

def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def store_manage(request):
    # products = request.user.store.product.all()   #.exclude(status=Product.DELETED)

    return render(request, 'store/manage.html')

@login_required
def store_products(request):
    products = request.user.store.product.all()   #.exclude(status=Product.DELETED)

    return render(request, 'store/products.html', {
        'products': products
    })

@login_required
def add_product(request):
    store = request.user.store

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()

            messages.success(request, '新增商品完成')

            return redirect('store_products')
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.filter(store=request.user.store)

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

            return redirect('store_products')
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

            return redirect('store_products')
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(store=request.user.store)

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

    return redirect('store_manage')

@login_required
def store_options(request):

    return render(request, 'store/options.html')