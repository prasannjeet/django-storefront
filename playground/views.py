from typing import ItemsView, Any, List, Dict

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.models import QuerySet, Q, F, Prefetch, Min, Max, Count, Avg, Sum, Value, Func
from django.db.models.functions import Concat
from django.db.models.query import RawQuerySet
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from storefront.models import Product, Collection, Order, OrderItem, Customer

# Create your views here.
# A view function is one that takes a request and returns a response
# Request handler
# Action

# First create a view (or a view function), then map this view to a URL.
from tags.models import TaggedItem


def say_hello(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello World')


def get_hello(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Product] = Product.objects.all()
    product_dict: dict[int, str] = {}
    product: Product
    for product in query_set:
        product_dict[product.id] = product.title
    context: dict[str, ItemsView[int, str]] = {'data': product_dict.items()}

    return render(request, 'hello.html', context)


# Example of exceptions
def get_hello2(request: HttpRequest) -> HttpResponse:
    try:
        item: Product = Product.objects.get(pk=0)
    except ObjectDoesNotExist:
        # pass
        return HttpResponse('Object does not exist')
    return HttpResponse(item.title)


# Another way if query is empty
def get_hello3(request: HttpRequest) -> HttpResponse:
    item: Product = Product.objects.filter(pk=0).first()
    return HttpResponse(item.title)


# Check if item exists or not
def get_hello4(request: HttpRequest) -> HttpResponse:
    is_exists: bool | Any = Product.objects.filter(pk=0).exists()
    if is_exists:
        return HttpResponse(Product.objects.get(pk=0).title)
    return HttpResponse('Item does not exist')


# Filtering example
# more:
# filter(collection__id=1)
# filter(collection__id__range=(1, 2))
def get_range(request: HttpRequest) -> HttpResponse:
    # keyword=value
    query_set: QuerySet[Product] = Product.objects.filter(unit_price__range=(20, 30))
    return render(request, 'three.html', {'products': list(query_set)})


# Customers with .com accounts
def get_com(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Customer] = Customer.objects.filter(email__contains='.com')
    return render(request, 'three.html', {'customers': list(query_set)})


# Collections without a featured product
def get_collection_without_featured(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Collection] = Collection.objects.filter(featured_product__isnull=True)
    return render(request, 'three.html', {'collections': list(query_set)})


# Products with low inventory (less than 10)
def products_with_low_inventory(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Product] = Product.objects.filter(inventory__lt=10)
    return render(request, 'three.html', {'products': list(query_set)})


# Orders placed by customer with id = 1
def orders_placed_with_customer_one(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Order] = Order.objects.filter(customer_id=1)
    return render(request, 'three.html', {'orders': list(query_set)})


# Order items for products in collection 3
# Another way: OrderItem.objects.filter(product__collection__id=3)
def order_item_collection_three(request: HttpRequest) -> HttpResponse:
    query_set_product: QuerySet[Product] = Product.objects.filter(collection_id=3)
    product_ids: list[int] = [x.id for x in list(query_set_product)]
    query_set_order_items: QuerySet[OrderItem] = OrderItem.objects.filter(product_id__in=product_ids)
    return render(request, 'three.html', {'order_items': list(query_set_order_items)})


# Limiting results
def limit_results(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Product] = Product.objects.filter(unit_price__range=(20, 30))[:10]
    return render(request, 'three.html', {'products': list(query_set)})


# Item.objects.count() returns a number, and not a query set.
# Item.objects.get(pk=something) -> pk is the primary key. It is a single item and not query set.

# This is just a test
def get_request(request: HttpRequest) -> HttpResponse:
    data: dict[str, str] = {'key1': 'value1', 'key2': 'value2'}
    context: dict[str, ItemsView[str, str]] = {'data': data.items()}
    return render(request, 'two.html', context)


# Select fields to query
# There is another option Product.objects.values_list()
def select_fields(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Product] = Product.objects.values('id', 'title', 'collection__title')
    return render(request, 'three.html', {'products': list(query_set)})


# Find products that have been ordered, order by title.
def ordered_products(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Product] = Product.objects.filter(
        id=F('orderitem__product_id'), orderitem__order__payment_status='P').distinct().order_by('title')
    return render(request, 'three.html', {'products': list(query_set)})


# Product.object.only() will return a query set with only the fields specified.
# Product.object.defer() will return a query set with all fields except the ones specified.
# Product.object.values() returns a list of dictionaries.
# Product.object.select_related() you can join tables to get related data. (one-to-one relationships only)
# Product.object.prefetch_related() you can join tables to get related data. (one-to-many relationships only)


# Exercise: Find last 5 orders with their customer and items.
# Both the prefetch query (commented and not commented) should return the same results.
def last_five_orders(request: HttpRequest) -> HttpResponse:
    # query_set: QuerySet = Order.objects.select_related('customer').prefetch_related(
    #     Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))).order_by('-placed_at')[:5]
    query_set: QuerySet = Order.objects.select_related('customer').prefetch_related(
        'orderitem_set__product').order_by('-placed_at')[:5]
    return render(request, 'three.html', {'orders': list(query_set)})


# If you want to use AND, then you can simply use filter().filter() and so on.
# Now we will se how to use OR
def or_example(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Product] = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    return render(request, 'three.html', {'products': list(query_set)})


# Aggregating Methods (Count Max Min Average Sum)
# Aggregate can also be done after filtering etc.
def aggregate(request: HttpRequest) -> HttpResponse:
    count: Dict[str, int] = Product.objects.aggregate(Count('id'), Max('unit_price'), Min('unit_price'))
    return render(request, 'three.html', {'count': count})


# How many orders do we have?
# How many units of product 1 have we sold?
# How many orders has customer 1 placed?
# What is the min, max and average price of the products in collection 3?
def question_14(request: HttpRequest) -> HttpResponse:
    count: int = Order.objects.count()
    print('There are %d orders.' % count)

    count: Dict[str, int] = OrderItem.objects.filter(product_id=1).aggregate(count=Sum('quantity'))
    print('%d units of product 1 was/where sold.' % count['count'])

    order_count: int = Order.objects.filter(customer_id=1).count()
    print('Customer 1 has placed %d orders.' % order_count)

    details: Dict[str, float] = Product.objects.filter(collection_id=3).aggregate(Max('unit_price'), Min('unit_price'),
                                                                                  Avg('unit_price'))
    print('The min, max and average price of the products in collection 3 is %.2f, %.2f and %.2f.' % (
        details['unit_price__max'], details['unit_price__min'], details['unit_price__avg']))

    return render(request, 'three.html')


# Add additional attributes to objects while querying. Use annotate().
def annotate(request: HttpRequest) -> HttpResponse:
    query_set1: QuerySet[Customer] = Customer.objects.annotate(is_new=Value(True))
    # Added another column is_new and the value is treu for all
    print(list(query_set1))

    query_set2: QuerySet[Customer] = Customer.objects.annotate(new_id=F('id') + 1)
    print(list(query_set2))

    return render(request, 'three.html')


# Calling Database Functions
# Google Django Database Functions to find out more about this.
def database_functions(request: HttpRequest) -> HttpResponse:
    # CONCAT
    query_set: QuerySet[Customer] = Customer.objects.annotate(
        full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    )
    for item in list(query_set):
        print(item.full_name)

    query_set2: QuerySet[Customer] = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )
    for item in list(query_set2):
        print(item.full_name)

    return render(request, 'three.html')


# Grouping Data
def grouping(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet[Customer] = Customer.objects.annotate(
        orders_count=Count('order', distinct=True)
    )
    for item in list(query_set):
        print(item.orders_count)

    return render(request, 'three.html')


# Expression Wrappers

# Querying generic relationships
def generic_relationship(request: HttpRequest) -> HttpResponse:
    content_type: ContentType = ContentType.objects.get_for_model(Product)

    tag__filter: QuerySet[TaggedItem] = TaggedItem.objects \
        .select_related('tag'). \
        filter(
        content_type=content_type, object_id__in=Product.objects.values_list('id', flat=True)
    )

    print(len(list(tag__filter)))
    for item in list(tag__filter):
        print(item.tag.name)

    return render(request, 'three.html')


# Encapsulate logic in custom managers
# def encapsulate(request: HttpRequest) -> HttpResponse:


# Add items to the database
def add_items(request: HttpRequest) -> HttpResponse:
    collection: Collection = Collection()
    # or Collection(title='Video Games'), etc.
    collection.title = 'Video Games'
    collection.featured_product = Product.objects.get(id=1)  # Or Product(pk=1)
    collection.save()

    # or Collection.objects.create(title='Video Games', featured_product=Product.objects.get(id=1))
    # This will also return the collection object
    # To update it, set model's id or primary key and then call save(). It will now be updated.
    # To update anything, first you need to get the object from database, so that you don't lose other values.
    # For example, if you want to update only title, you might end up deleting all other fields of that object.
    # OR use Collection.objects.update
    # Collections.objects.filter(id=1).update(title='Video Games') --> This is good

    return render(request, 'three.html')


# Deleting Objects
def delete_items(request: HttpRequest) -> HttpResponse:
    collection: Collection = Collection(pk=11)
    collection.delete()

    return render(request, 'three.html')


# Transactional
# @transaction.atomic() This is a way
def transactional(request: HttpRequest) -> HttpResponse:
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(request, 'three.html')


# Executing SQL Queries
def execute_sql(request: HttpRequest) -> HttpResponse:
    query_set: RawQuerySet = Product.objects.raw('SELECT * FROM storefront_product')
    for item in list(query_set):
        print(item.title)

    # If your query does not map to a particular model, you can use RawQuerySet.execute
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM storefront_product')
        for row in cursor.fetchall():
            print(row)

    return render(request, 'three.html')

# Command to create admin user for admin site
# python manage.py createsuperuser
