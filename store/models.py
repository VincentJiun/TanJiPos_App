from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Store(models.Model):
    manager = models.OneToOneField(User, related_name='store', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    address = models.CharField(max_length=150, blank=True, null=True)

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
    DRAFT = '待上架'
    ACTIVATE = '上架中'
    DELETED = '刪除'

    STATUS_CHOICES = (
        (DRAFT, '待上架'),
        (ACTIVATE, '上架中'),
        (DELETED, '刪除'),
    )

    store = models.ForeignKey(Store, related_name='product', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/products_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVATE)

    class Meta:
        ordering = ('category',) # 排序

    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     if self.category.store != self.store:
    #         raise ValueError("The category Error")
        
    #     super().save(*args, **kwargs)