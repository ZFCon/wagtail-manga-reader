from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()
class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    item_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'item_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content_object.title
    
