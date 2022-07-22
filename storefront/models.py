from datetime import datetime, date
from decimal import Decimal
from typing import List, Tuple

from django.db import models
from django.db.models import Manager


class Collection(models.Model):
    title: str = models.CharField(max_length=255)
    # products = models.ManyToManyField(Product)
    featured_product: 'Product' = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description: str = models.CharField(max_length=255)
    discount: float = models.FloatField()


# Create your models here.
# ID field is automatically created by Django, and is a primary key
# But we can also create our own primary key

class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True), if you want to create your own primary key
    title: str = models.CharField(max_length=255)  # Varchar255
    slug: str = models.SlugField()  # SlugField
    description: str = models.TextField()  # Text
    # Eg. Max price = 9999.99 (total 6 digits, after decimal point = 2 digits, so we need to set that)
    unit_price: Decimal = models.DecimalField(max_digits=6, decimal_places=2)
    inventory: int = models.IntegerField()
    last_update: datetime = models.DateTimeField(auto_now=True)  # Or auto_now_add=True for update this field only 
    # first time 
    collection: Collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions: Manager = models.ManyToManyField(Promotion)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


# Choices - just like ENUM in Java

class Customer(models.Model):
    MEMBERSHIP_BRONZE: str = 'B'
    MEMBERSHIP_SILVER: str = 'S'
    MEMBERSHIP_GOLD: str = 'G'
    MEMBERSHIP_CHOICES: list[tuple[str, str]] = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name: str = models.CharField(max_length=255)
    last_name: str = models.CharField(max_length=255)
    email: str = models.EmailField(unique=True)
    phone: str = models.CharField(max_length=255)
    birth_date: date = models.DateField(null=True, blank=True)
    membership: str = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']


class Order(models.Model):
    STATUS_PENDING: str = 'P'
    STATUS_COMPLETED: str = 'C'
    STATUS_CANCELLED: str = 'F'
    STATUS_CHOICES: list[tuple[str, str]] = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled')
    ]
    placed_at: datetime = models.DateTimeField(auto_now_add=True)
    payment_status: str = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer: Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


# Now we implement one-to-one relationship

# class Address(models.Model):
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
#     # One-to-one relationship, if customer is deleted, address will be deleted
#     # Since we made customer primary key, we ensure that one customer only has one address, since another address
#     # will not be allowed.


# Now we implement one-to-many relationship

class Address(models.Model):
    street: str = models.CharField(max_length=255)
    city: str = models.CharField(max_length=255)
    customer: Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product: Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity: int = models.PositiveSmallIntegerField()
    unit_price: Decimal = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at: datetime = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart: Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity: int = models.PositiveSmallIntegerField()
