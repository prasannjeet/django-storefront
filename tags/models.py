from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.db.models import QuerySet


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type: ContentType = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag'). \
            filter(
                content_type=content_type,
                object_id__in=obj_id
            )


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