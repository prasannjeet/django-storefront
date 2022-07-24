# Google Django ModelAdmin and find all options
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from storefront.admin import InventoryFilter
from storefront.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    search_fields = ['title__icontains']
    prepopulated_fields = {
        'slug': ['title', ]
    }
    # inlines = [TagInLine] # After defining custom app for this, we comment this line.
    # fields = ['title', 'slug']
    # exclude = ['promotions']
    # readonly_fields = ['slug']
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
