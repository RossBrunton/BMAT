from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaultfilters
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.template import defaultfilters
from django.contrib.auth.models import User

import json

colours = [
    ("white", "Boring White"),
]

class Tag(models.Model):
    owner = models.ForeignKey(User)
    name = models.TextField(max_length=100)
    implies = models.ManyToManyField("self", related_name="implicators")
    colour = models.TextField(max_length=20, choices=colours)
    slug = models.SlugField()

    def __str__(self):
        return "Tag '"+self.name+"' for "+self.owner.username
    
    def to_dir(self):
        out = {}
        out["name"] = self.name
        out["colour"] = self.colour
        out["slug"] = self.slug
        out["id"] = self.pk
        
        return out
    
    def to_json(self):
        return json.dumps(self.to_dir)
