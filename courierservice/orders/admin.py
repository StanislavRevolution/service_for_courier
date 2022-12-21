from django.contrib import admin

from .models import Product, Order, ProductAmount
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductAmount)
