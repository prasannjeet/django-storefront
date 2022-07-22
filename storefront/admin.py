from typing import Tuple, List

from django.contrib import admin, messages

# Register your models here.
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from storefront.models import Collection, Product, Customer, Order


class InventoryFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request: object, queryset: QuerySet) -> object:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        return queryset

    title: str = 'inventory'
    parameter_name: str = 'inventory'




# Override the base query set used to render the list page
# If we want to show the number of products in each collection in the collection.

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display: tuple[str, str] = ('title', 'products_count')

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # admin:app_model_page
        url = (
                reverse('admin:storefront_product_changelist')
                + '?'
                + urlencode({
                    'collection__id': str(collection.id)
                })
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

    products_count.short_description = 'Number of products'


# admin.site.register(Collection)


# Google Django ModelAdmin and find all options
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display: tuple[str, str, str, str, str, str] = (
        'id', 'title', 'unit_price', 'inventory_status', 'collection', 'collection_title')
    list_editable: tuple[str] = ('unit_price',)
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page: int = 10
    list_select_related: list[str] = [
        'collection']  # By doing this django will automatically query collection along with product

    # And if we don't do that, django will still work, but it will query collection_title one-by-one.

    # Now we will add a computed column in the admin view for Product
    @admin.display(ordering='inventory')
    def inventory_status(self, product) -> str:
        return 'OK' if product.inventory > 10 else 'Low'

    def collection_title(self, product) -> str:
        return product.collection.title

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated_count: object = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.SUCCESS
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display: tuple[str, str, str, str] = ('name', 'email', 'membership', 'orders_count')
    list_editable: tuple[str] = ('membership',)
    list_per_page: int = 10
    ordering: list[str] = ['last_name', 'first_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'email__istartswith']

    # Order by first and last name
    @admin.display(ordering='first_name')
    def name(self, customer) -> str:
        return f'{customer.first_name} {customer.last_name}'

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

    @admin.display(ordering='orders_count')
    def orders_count(self, customer) -> int:
        url = (
            reverse('admin:storefront_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    orders_count.short_description = 'Number of orders'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: tuple[str, str, str, str] = ('id', 'placed_at', 'payment_status', 'customer')
    list_editable: tuple[str] = ('payment_status',)
    list_select_related: list[str] = ['customer']
    list_per_page: int = 10
