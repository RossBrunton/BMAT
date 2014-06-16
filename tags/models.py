from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaultfilters
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.template import defaultfilters
from django.contrib.auth.models import User

colours = [
    ("white", "Boring White"),
]

class Tag(models.Model):
    owner = models.ForeignKey(User)
    name = models.TextField(max_length=100)
    implies = models.ManyToManyField("self", related_name="implicators")
