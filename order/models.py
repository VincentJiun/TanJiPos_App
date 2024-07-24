from django.db import models

from store.models import Product

# Create your models here.

class Order(models.Model):
    merchant_id = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    total_cost = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

