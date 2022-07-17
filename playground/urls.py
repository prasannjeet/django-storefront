from typing import List, Any

from django.urls import path

from playground import views

# URL Conf Module, or URLConf
urlpatterns: list[Any] = [
    path('hello/', views.say_hello),
    path('get-hello/', views.get_hello),
    path('get-hello2/', views.get_hello2),
    path('get-hello3/', views.get_hello3),
    path('get-hello4/', views.get_hello4),
    path('get-range/', views.get_range),
    path('get-request/', views.get_request),
    path('get_com/', views.get_com),
    path('get_collection_without_featured/', views.get_collection_without_featured),
    path('products_with_low_inventory/', views.products_with_low_inventory),
    path('orders_placed_with_customer_one/', views.orders_placed_with_customer_one),
    path('order_item_collection_three/', views.order_item_collection_three),
    path('limit_results/', views.limit_results),
    path('or_example/', views.or_example),
    path('select_fields/', views.select_fields),
    path('ordered_products/', views.ordered_products),
    path('last_five_orders/', views.last_five_orders),
    path('aggregate/', views.aggregate),
    path('question_14/', views.question_14),
    path('annotate/', views.annotate),
    path('database_functions/', views.database_functions),
    path('grouping/', views.grouping),
    path('generic_relationship/', views.generic_relationship),
    path('add_items/', views.add_items),
    path('execute_sql/', views.execute_sql),
]
