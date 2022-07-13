from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class TaggedItem(models.Model):
    # What tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (product, video, blog, etc.)
    # ID of the object
    # From type we find table, from id we use item
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
