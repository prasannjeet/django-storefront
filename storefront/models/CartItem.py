from django.db import models

from storefront.models.Cart import Cart
from storefront.models.Product import Product


class CartItem(models.Model):
    cart: Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity: int = models.PositiveSmallIntegerField()
