from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, min_length=1)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remaining_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wishlist = models.ManyToManyField(Product, related_name='wishlisted_by', blank=True)
    shopping_cart = models.ManyToManyField(Product, related_name='in_cart_by', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"