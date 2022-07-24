from datetime import datetime

from django.db import models

from storefront.models.Customer import Customer


class Order(models.Model):
    STATUS_PENDING: str = 'P'
    STATUS_COMPLETED: str = 'C'
    STATUS_CANCELLED: str = 'F'
    STATUS_CHOICES: list[tuple[str, str]] = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled')
    ]
    placed_at: datetime = models.DateTimeField(auto_now_add=True)
    payment_status: str = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    customer: Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
