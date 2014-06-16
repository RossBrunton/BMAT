from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaultfilters
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.template import defaultfilters
from django.contrib.auth.models import User

from tags.models import Tag

class Bookmark(models.Model):
    owner = models.ForeignKey(User)
    title = models.TextField(max_length = 50)
    url = models.TextField(max_length = 500)
    tags = models.ManyToManyField(Tag)

