from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from tags.models.Tag import Tag
from tags.models.TaggedItemManager import TaggedItemManager


class TaggedItem(models.Model):
    objects: TaggedItemManager = TaggedItemManager()
    # What tag applied to what object
    tag: Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (product, video, blog, etc.)
    # ID of the object
    # From type we find table, from id we use item
    content_type: ContentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id: int = models.PositiveIntegerField()
    content_object: GenericForeignKey = GenericForeignKey()
