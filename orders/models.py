from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname']

    def __str__(self) -> str:
        return f'El usuario: {self.name} {self.lastname}'

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rolname = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f'{self.user} tiene rol de {self.rolname}'

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

class Size(models.Model):
    name = models.CharField(max_length=50)

class Topping(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_toppings = models.IntegerField(default=0)
    sizes = models.ManyToManyField(Size, through='ProductVariantPrice')

class ProductVariantPrice(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    quantity = models.IntegerField()
