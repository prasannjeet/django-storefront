# Now we implement one-to-many relationship
from django.db import models

from storefront.models.Customer import Customer


class Address(models.Model):
    street: str = models.CharField(max_length=255)
    city: str = models.CharField(max_length=255)
    customer: Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
