from django.contrib import admin

from .models import Store, Category, Product, Option, OptionValue, Table

# Register your models here.
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Option)
admin.site.register(OptionValue)
admin.site.register(Table)



