# Choices - just like ENUM in Java
from datetime import date

from django.db import models


class Customer(models.Model):
    MEMBERSHIP_BRONZE: str = 'B'
    MEMBERSHIP_SILVER: str = 'S'
    MEMBERSHIP_GOLD: str = 'G'
    MEMBERSHIP_CHOICES: list[tuple[str, str]] = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name: str = models.CharField(max_length=255)
    last_name: str = models.CharField(max_length=255)
    email: str = models.EmailField(unique=True)
    phone: str = models.CharField(max_length=255)
    birth_date: date = models.DateField(null=True, blank=True)
    membership: str = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']
