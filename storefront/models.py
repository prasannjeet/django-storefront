from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # products = models.ManyToManyField(Product)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


# Create your models here.
# ID field is automatically created by Django, and is a primary key
# But we can also create our own primary key

class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True), if you want to create your own primary key
    title = models.CharField(max_length=255)  # Varchar255
    description = models.TextField
    # Eg. Max price = 9999.99 (total 6 digits, after decimal point = 2 digits, so we need to set that)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    modified = models.DateTimeField(auto_now=True)  # Or auto_now_add=True for update this field only first time
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


# Choices - just like ENUM in Java

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETED = 'C'
    STATUS_CANCELLED = 'X'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


# Now we implement one to one releationship

# class Address(models.Model):
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
#     # One to one relationship, if customer is deleted, address will be deleted
#     # Since we made customer primary key, we ensure that one customer only has one address, since another address
#     # will not be allowed.


# Now we implement one to many relationship

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
