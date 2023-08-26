""" Database models for bookmarks """

from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from pytz import utc

from tags.models import Tag, Taggable
from tags import taggable
from bookmarks.templatetags.bookmark import bookmark
from users.models import Settings

import json

from datetime import datetime
import six

_DT_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

@taggable("autotag")
class Autotag(Taggable):
    """ Automatic tag rule
    
    Contains:
    - owner:ForeignKey to User
    - pattern:CharField
    - tags:ManyToManyField to Tag
    - added:DateTimeField
    
    The owner of a rule is the user that added it.
    
    Simply put, if a bookmark is added, and the `pattern` of any Autotag owned by the same user matches it, then the
    tags of the autotag are added to the bookmark.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pattern = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name="autotags")
    added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-added"]
    
    def __str__(self):
        return ("Autotag '"+self.pattern+"' for "+self.owner.username).encode("ascii", "ignore").decode("ascii")
    
    def to_dir(self):
        """ Returns a dictionary representation of this autotag
        
        The keys of the object are the field names, and the values are the respective values.
        
        Tags are a list of dicts representing tags as per Tag.to_dir().
        """
        out = {}
        out["pattern"] = self.pattern
        out["id"] = self.pk
        out["added"] = self.added.astimezone(utc).strftime(_DT_FORMAT)
        out["tags"] = []
        
        for t in self.tags.all():
            out["tags"].append(t.to_dir())
        
        return out
    
    def to_json(self):
        """ Produces the JSON representation of this bookmark
        
        It's the JSON for the output of to_dir()
        """
        return json.dumps(self.to_dir())
    
    @staticmethod
    def from_json(jsonData, user):
        """ Given the JSON representation of the autotag, creates one for it
        
        Note that this SAVES the object to the database.
        
        If the "added" property of the object is absent, one will be created with the current date.
        """
        obj = json.loads(jsonData)
        
        at = Autotag(owner=user, pattern=obj["pattern"])
        
        at.save()
        
        if "added" in obj:
            at.added = make_aware(datetime.strptime(obj["added"], _DT_FORMAT), utc)
        
        for t in obj["tags"]:
            if isinstance(t, six.string_types):
                at.tag(t)
            else:
                at.tag(t["id"])
        
        at.save()
        
        return at
    
    @staticmethod
    def check_url(user, url):
        """ Loops through all the autotag instances owned by the user, and returns a list of tags that apply
        """
        #TODO: Should see if I should do this in the database
        url = url.lower()
        
        out = []
        
        for at in Autotag.by_user(user):
            if at.pattern.lower() in url:
                for t in at.tags.all():
                    out.append(t)
        
        return out
    
    @staticmethod
    def by_user(user):
        """ Get all the autotags owned by a given user """
        return Autotag.objects.all().filter(owner=user)
