from django.conf import settings

from store.models import Product

class OrderCart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = []

        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart)
    
    def add_item(self, product_id, options, quantity=1):
        id = str(product_id)

        for item in self.cart:
            if item['product_id']==id and item['options']==options:
                item['quantity'] += int(quantity)
                return
            
        item = {
            'product_id': product_id,
            'quantity': int(quantity),
            'options': options
        }    
        self.cart.append(item)
        print(self.cart)

    def remove_item(self, product_id, options):
        self.cart = [item for item in self.cart if not (item['product_id'] == product_id and item['options'] == options)]

    

