from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Store(models.Model):
    manager = models.OneToOneField(User, related_name='store', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    title = models.CharField(max_length=50)
    store = models.ForeignKey(Store, related_name='category', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title
    
class Product(models.Model):
    store = models.ForeignKey(Store, related_name='product', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/products_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title