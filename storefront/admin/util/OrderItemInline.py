from django.contrib.admin import TabularInline

from storefront.models import OrderItem


class OrderItemInline(TabularInline): # Also StandardInline
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0
    min_num = 1
    max_num = 10
