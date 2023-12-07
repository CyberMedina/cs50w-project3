from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User

# Create your models here.



class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

    


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Topping(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.name}'
class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'Category: {self.category} - Name: {self.name} '

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_toppings = models.IntegerField(default=0)
    sizes = models.ManyToManyField(Size, through='ProductVariantPrice')

    def __str__(self):
        # Obtiene los tamaños y los convierte en una lista de cadenas
        size_strings = [str(size) for size in self.sizes.all()]
        # Une la lista en una única cadena separada por comas
        sizes_str = ', '.join(size_strings)
        return f'{self.product} - toppings: {self.number_of_toppings} - Size: {sizes_str}'

class ProductVariantPrice(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.product_variant.product} - Price: {self.price} - Size: {self.size}' 
    
    def jsonProductVariantPrice(self):
        return {
            'id': self.id,
            'Category': self.product_variant.product.category.name,
            'productName': self.product_variant.product.name,
            'price': self.price,
            'size': self.size.name
        }
    
    

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user}'
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    quantity = models.IntegerField()


    def __str__(self) -> str:
        return f'{self.order} {self.product_variant} {self.size} {self.toppings} {self.quantity}'
