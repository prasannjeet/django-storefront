from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.db.models import Model


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        tagged_item: Model = apps.get_model('tags', 'TaggedItem')
        content_type: ContentType = ContentType.objects.get_for_model(obj_type)

        return tagged_item.objects.select_related('tag').filter(
            content_type=content_type,
            object_id__in=obj_id
        )
