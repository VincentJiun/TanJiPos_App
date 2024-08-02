from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from store.models import Store, Product

from .cart import Cart
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

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    product = get_object_or_404(Product, pk=product_id)
    slug = product.store.slug

    print(cart)

    return redirect('order_home', slug=slug)

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    
    return redirect('cart_view')


def cart_view(request):
    cart = Cart(request)

    return render(request, 'order/cart_view.html', {
        'cart':cart
    })

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def checkout(request):
    cart = Cart(request)

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

            return redirect('cart_view')
    else:
        form = OrderForm()

    return render(request, 'order/checkout.html', {
        'cart': cart,
        'form': form
    })