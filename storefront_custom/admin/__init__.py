from django.contrib import admin

# Register your models here.
from storefront.models import Product
from storefront_custom.admin.CustomProductAdmin import CustomProductAdmin

# This is the best way to do it, because just in case the other apps, like tags and this app itself is not available,
# python will not throw an error or fail. Try it and see for yourself.

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
