from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from store.models import Store, Product, Option, OptionValue, Table

from .cart import Cart
from .order_cart import OrderCart
from .models import Order, OrderItem
from .forms import OrderForm

def order_home(request, slug):
    check = False
    cart = Cart(request)
    table = request.GET.get('table', '')
    table_name = ''

    store = get_object_or_404(Store, slug=slug)
    categories = store.category.all()
    products = store.product.filter(status=Product.ACTIVATE)
    if table:
        if store.table.filter(slug=table).exists():
            table_slug = store.table.get(slug=table)
            table_name = table_slug.title
            check = True

    return render(request, 'order/order_home.html', {
        'store': store,
        'categories': categories,
        'products': products,
        'table_name':table_name,
        'check':check,
        'table':table
    })

def product_info(request, slug, product_id):
    table = request.GET.get('table', '')
    store = get_object_or_404(Store, slug=slug)
    product = get_object_or_404(Product, id=product_id)
    options = Option.objects.filter(store=store)
    option_values = OptionValue.objects.all()
    # print(table)

    return render(request, 'order/product_info.html',{
        'table': table,
        'store': store,
        'product':product,
        'options': options,
        'option_values': option_values
    })

def add_to_cart(request, product_id):
    table = request.GET.get('table')  
    product = get_object_or_404(Product, pk=product_id)
    slug = product.store.slug
    options = Option.objects.filter(store=product.store)
    product_options = {}
    # print(options)

    if request.method == 'POST':
        for option in options:
            values = OptionValue.objects.filter(option=option)
            for value in values:
                if request.POST.get(str(value.pk))=='on':
                    product_options.update({option.title:value.title})
            
    print(product_options)
        
    cart = Cart(request)
    cart.add(product_id, options=product_options)

    # cart = OrderCart(request)
    # cart.add_item(product_id, product_options)

    return redirect(f'/order/{slug}/?table={table}')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    table = request.GET.get('table', '')
    product = get_object_or_404(Product, pk=product_id)
    slug = product.store.slug

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    
    return redirect(f'/order/{slug}/cart/?table={table}')


def cart_view(request, slug):
    cart = Cart(request)
    store = get_object_or_404(Store, slug=slug)
    order_tables = Table.objects.filter(store = store)
    table = request.GET.get('table', '')

    return render(request, 'order/cart_view.html', {
        'cart':cart,
        'store':store,
        'order_tables':order_tables,
        'table':table
    })

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    table = request.GET.get('table', '')

    product = get_object_or_404(Product, pk=product_id)
    slug = product.store.slug

    return redirect(f'/order/{slug}/cart/?table={table}')

def checkout(request, slug):
    cart = Cart(request)
    table = request.GET.get('table', '')
    store = get_object_or_404(Store, slug=slug)
    

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0
            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.total_cost = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

            cart.clear()    

            return redirect(f'/order/{slug}/?table={table}')
    else:
        form = OrderForm()

    return render(request, 'order/checkout.html', {
        'table':table,
        'store':store,
        'cart': cart,
        'form': form
    })