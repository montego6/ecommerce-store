from django.contrib import admin
from .models import Category, Item, Address, OrderItem, Order

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Order)
