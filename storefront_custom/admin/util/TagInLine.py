from typing import List

from django.apps import apps
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Model


class TagInLine(GenericTabularInline):
    autocomplete_fields: list[str] = ['tag']
    model: Model = apps.get_model('tags', 'TaggedItem')  # Best way to import other models without dependency
    extra: int = 0
