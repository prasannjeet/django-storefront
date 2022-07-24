from django.db import models

from storefront.models import Product


class Collection(models.Model):
    title: str = models.CharField(max_length=255)
    # products = models.ManyToManyField(Product)
    featured_product: 'Product' = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
