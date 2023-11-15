from django.contrib import admin
from .models import User, Rol, Product, Order, ProductCategory, ProductVariant, ProductVariantPrice, Size, Topping, Product, Order, OrderItem

# Register your models here.
admin.site.register(User)
admin.site.register(Rol)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductCategory)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(OrderItem)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)


