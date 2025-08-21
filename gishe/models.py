from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remaining_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Customer(models.Model):
    state_vip = "V"
    state_cip = "C"
    state_normal = "N"
    state_choices = [
        (state_vip, "VIP Customer"),
        (state_cip, "CIP Customer"),
        (state_normal, "Normal Customer"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state_of_membership = models.CharField(max_length=1, choices=state_choices, default=state_normal)
    # state_of_membership = models.CharField(max_length= 6, choices=[("vip", "VIP Customer"), ("cip", "CIP Customer"), ("normal", "Normal Customer")], default="normal")
    wishlist = models.ManyToManyField(Product, related_name='wishlisted_by', blank=True)
    shopping_cart = models.ManyToManyField(Product, related_name='in_cart_by', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    state_pending = "P"
    state_shipped = "S"
    state_delivered = "D"
    state_cancelled = "C"
    state_choices = [
        (state_pending, "Pending"),
        (state_shipped, "Shipped"),
        (state_delivered, "Delivered"),
        (state_cancelled, "Cancelled"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    state_order = models.CharField(max_length=1, choices=state_choices, default=state_pending)
    order_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"