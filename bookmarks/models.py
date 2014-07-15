from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import defaultfilters

from tags.models import Tag

from HTMLParser import HTMLParser
import json
import requests

class Bookmark(models.Model):
    class Meta:
        ordering = ["-added"]
    
    owner = models.ForeignKey(User)
    title = models.TextField(max_length = 50)
    url = models.TextField(max_length = 500)
    tags = models.ManyToManyField(Tag, related_name="bookmarks")
    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Bookmark '"+self.title+"' for "+self.owner.username
    
    def tag(self, tag):
        print type(tag)
        
        if isinstance(tag, (int, long)):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except ObjectDoesNotExist:
                #Handle this better?
                return
        
        if isinstance(tag, (str, unicode)):
            try:
                tag = Tag.objects.get(slug=defaultfilters.slugify(tag), owner=self.owner)
            except ObjectDoesNotExist:
                tag = Tag(owner=self.owner, name=tag)
                tag.save()
        
        tag.owner = self.owner
        tag.save()
        self.tags.add(tag)
    
    def untag(self, tag):
        if isinstance(tag, (int, long)):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except ObjectDoesNotExist:
                return
        
        if type(tag) == str:
            try:
                tag = Tag.objects.get(name__iexact=tag, owner=self.owner)
            except ObjectDoesNotExist:
                return
        
        self.tags.remove(tag)
    
    def download_title(self):
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
        out = {}
        out["title"] = self.title
        out["url"] = self.url
        out["id"] = self.pk
        out["tags"] = []
        
        for t in self.tags.all():
            out["tags"].append(t.to_dir())
        
        return out
    
    def to_json(self):
        return json.dumps(self.to_dir())


def bookmarks_by_user(user):
    return Bookmark.objects.all().filter(owner=user)


class HTMLTitleReader(HTMLParser):
    def __init__(self):
        self.title = ""
        self._open = False
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._open = True
        
    def handle_endtag(self, tag):
        if tag == "title":
            self._open = False
        
    def handle_data(self, data):
        if self._open:
            self.title = data
