from django.db import models


class Promotion(models.Model):
    description: str = models.CharField(max_length=255)
    discount: float = models.FloatField()
