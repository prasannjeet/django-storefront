from storefront.admin import ProductAdmin
from storefront_custom.admin.util.TagInLine import TagInLine


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]
