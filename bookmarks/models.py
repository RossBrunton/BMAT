""" Database models for bookmarks """

from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters

from tags.models import Tag, Taggable
from tags import taggable
from bookmarks.templatetags.bookmark import bookmark

from six.moves.html_parser import HTMLParser
import json
import requests

@taggable("bookmark")
class Bookmark(Taggable):
    """ A single bookmark
    
    Contains:
    - owner:ForeignKey to User
    - title:TextField
    - url:TextField
    - tags:ManyToManyField to Tag
    - added:DateTimeField
    
    The owner of a bookmark is the user that added it. A bookmark can only be associated with one user, even if multiple
    users register the same URL.
    
    Bookmarks are ordered latest to oldest.
    """
    owner = models.ForeignKey(User)
    title = models.TextField(max_length = 50)
    url = models.TextField(max_length = 500)
    tags = models.ManyToManyField(Tag, related_name="bookmarks")
    added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-added"]
    
    def __str__(self):
        return ("Bookmark '"+self.title+"' for "+self.owner.username).encode("ascii", "ignore")
    
    def download_title(self):
        """ Downloads the title of the bookmark
        
        This may fail silently. If it does, it sets the title to "Unknown Title".
        """
        self.title = "Unknown Title"
        
        try:
            r = requests.get(self.url, timeout=3.0)
            r.raise_for_status()
            
            p = HTMLTitleReader()
            p.feed(r.text)
            
            self.title = p.title
            self.save()
            
        except:
            return
    
    def to_dir(self):
        """ Returns a dictionary representation of this tag
        
        The keys of the object are the field names, and the values are the respective values.
        
        Tags are a list of dicts representing tags as per Tag.to_dir().
        """
        out = {}
        out["title"] = self.title
        out["url"] = self.url
        out["id"] = self.pk
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
    def by_user(user):
        """ Get all the bookmarks owned by a given user """
        return Bookmark.objects.all().filter(owner=user)


class HTMLTitleReader(HTMLParser):
    """ A HTML parser for extracting the title of a HTML page
    
    It sets a flag on when it encounters a title, and closes it when the title is closed, reading the data only when
    the flag is on.
    """
    def __init__(self):
        self._title = ""
        self._open = False
        self._nomore = False
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._open = True
        
    def handle_endtag(self, tag):
        if tag == "title":
            self._open = False
        
        if tag in ["title", "head"]:
            self._nomore = True
        
    def handle_data(self, data):
        if self._open and not self._nomore:
            self._title += data
    
    @property
    def title(self):
        if self._open:
            return ""
        
        return self._title
