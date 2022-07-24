from urllib.parse import urlencode

from django.contrib import admin
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from storefront.models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display: tuple[str, str] = ('title', 'products_count')
    search_fields = ['title__icontains']

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
