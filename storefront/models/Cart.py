from datetime import datetime

from django.db import models


class Cart(models.Model):
    created_at: datetime = models.DateTimeField(auto_now_add=True)
