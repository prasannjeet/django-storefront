# Create your models here.
# ID field is automatically created by Django, and is a primary key
# But we can also create our own primary key
from datetime import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Manager

from storefront.models.Collection import Collection
from storefront.models.Promotion import Promotion


class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True), if you want to create your own primary key
    title: str = models.CharField(max_length=255)  # Varchar255
    slug: str = models.SlugField()  # SlugField
    description: str = models.TextField(null=True, blank=True)  # Text
    # Eg. Max price = 9999.99 (total 6 digits, after decimal point = 2 digits, so we need to set that)
    unit_price: Decimal = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1, message='Price must not be smaller than 1')]
    )
    inventory: int = models.IntegerField(
        validators=[MinValueValidator(0, message='Inventory must not be negative')]
    )
    last_update: datetime = models.DateTimeField(auto_now=True)  # Or auto_now_add=True for update this field only
    # first time
    collection: Collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions: Manager = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

# Google django validators for all validating classes
