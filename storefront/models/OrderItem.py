from decimal import Decimal

from django.db import models

from storefront.models.Order import Order
from storefront.models.Product import Product


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product: Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity: int = models.PositiveSmallIntegerField()
    unit_price: Decimal = models.DecimalField(max_digits=6, decimal_places=2)
