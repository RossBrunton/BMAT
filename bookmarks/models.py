from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaultfilters
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.template import defaultfilters
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from tags.models import Tag

import requests
from HTMLParser import HTMLParser

class Bookmark(models.Model):
    owner = models.ForeignKey(User)
    title = models.TextField(max_length = 50)
    url = models.TextField(max_length = 500)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return "Bookmark '"+self.title+"' for "+self.owner.username
    
    def tag(self, tag):
        if isinstance(tag, (int, long)):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except ObjectDoesNotExist:
                #Handle this better?
                return
        
        if type(tag) == str:
            try:
                tag = Tag.objects.get(name__iexact=tag, owner=self.owner)
            except ObjectDoesNotExist:
                tag = Tag(owner=self.owner, name=tag)
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
        r = requests.get(self.url, timeout=3.0)

        try:
            r.raise_for_status()
            
            p = HTMLTitleReader()
            p.feed(r.text)
            
            self.title = p.title
            self.save()
            
        except:
            return


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
