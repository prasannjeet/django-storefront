from django.contrib import admin
from django.db.models import QuerySet


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
