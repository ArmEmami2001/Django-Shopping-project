from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Duration of the promotion in days")
    # product_set = models.ManyToManyField(Product, related_name='promotions', blank=True)

    def __str__(self):
        return f"Promotion {self.code}: {self.discount_amount} off"

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products',null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remaining_stock = models.PositiveIntegerField(default=0)
    promotion = models.ManyToManyField(Promotion, related_name='products', blank=True)
    #related name is for reverse access from promotion to products

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
    name = models.CharField(max_length=100)
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

    # class Meta:
    #     db_table = 'gishe_customers'
    #     indexes = [
    #         models.Index(fields=['name', 'email']),
    #     ]

class Order(models.Model):
    #one order has multiple order items
    #one product can be in multiple order items but one order item is for one product
    #one to one and one to many is written in child (the many side) IMPORTANTTTTTTTTTTTTTTTTTT
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
    # product = models.ManyToManyField(Product)
    #one to one is onetoonefield one to many is foreign key and many to amny is manytomany field
    #customer is foreign key why? because each order is associated with a specific customer
    #order is many to many field why? because an order can contain multiple products and a product can be part of multiple orders
    # quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    state_order = models.CharField(max_length=1, choices=state_choices, default=state_pending)
    order_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    
class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order Item {self.product.name}"

class Address(models.Model):
    customer = models.OneToOneField(Customer, primary_key=True, on_delete=models.CASCADE )
    # models.CASCADE will delete the address if the customer is deleted
    # models.SET_NULL will set the customer to null if the address is deleted
    # models.SET_DEFAULT will set the customer to a default value if the address is deleted
    # models.PROTECT will prevent the address from being deleted if it is referenced by a customer
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    #ONE TO ONE RELATION IS WRITTEN IN CHILD NOT PARENT SO IN ADDRESS
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"Address for {self.customer}: {self.street}, {self.city}, {self.state}, {self.zip_code}"

