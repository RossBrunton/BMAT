""" Database models for bookmarks """

from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import UTC, make_aware

from tags.models import Tag, Taggable
from tags import taggable
from bookmarks.templatetags.bookmark import bookmark
from users.models import Settings
from autotags.models import Autotag

from six.moves.html_parser import HTMLParser
from six.moves.urllib.robotparser import RobotFileParser
from six.moves.urllib.parse import urlparse
import json
import requests

from datetime import datetime
import six

_DT_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"

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
    title = models.CharField(max_length=200, db_index=True)
    url = models.CharField(max_length=500, db_index=True)
    tags = models.ManyToManyField(Tag, related_name="bookmarks")
    added = models.DateTimeField(auto_now_add=True)
    valid_url = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-added"]
    
    def __str__(self):
        return ("Bookmark '"+self.title+"' for "+self.owner.username).encode("ascii", "ignore").decode("ascii")
    
    def save(self, *args, **kwargs):
        """ Override of save method to validate url and set the appropriate setting """
        uv = URLValidator()
        
        try:
            uv(self.url)
            self.valid_url = True
        except:
            self.valid_url = False
        
        super(Bookmark, self).save(*args, **kwargs)
    
    @property
    def do_link(self):
        """ Returns a boolean indicating whether the bookmark should be formatted as a link
        
        It takes its owners preference and whether this is a valid URL into account.
        """
        return self.valid_url or self.owner.settings.url_settings == Settings.URL_SETTINGS_LINK
    
    @property
    def url_domain(self):
        """ Returns the scheme and domain for this bookmark's URL or None
        
        That is, https://somedomain.tld/path/to/file goes to https://somedomain.tld.
        
        Returns None if the URL isn't a valid URL.
        """
        if self.valid_url:
            return "{uri.scheme}://{uri.netloc}".format(uri=urlparse(self.url))
        else:
            return None
    
    def download_title(self):
        """ Downloads the title of the bookmark
        
        This may fail silently. If it does, it sets the title to "Unknown Title".
        """
        self.title = "Unknown Title"
        
        try:
            url = urlparse(self.url)
            robots = "{}://{}/robots.txt".format(url.scheme, url.netloc)
            
            rfp = RobotFileParser(robots)
            rfp.read()
            
            if rfp.can_fetch("BMAT", self.url):
                r = requests.get(self.url, timeout=3.0, headers={"User-Agent": "BMAT"})
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
        out["added"] = self.added.astimezone(UTC()).strftime(_DT_FORMAT)
        out["tags"] = []
        out["valid_url"] = self.valid_url
        
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
        """ Given the JSON representation of the bookmark, creates one for it
        
        Note that this SAVES the object to the database.
        """
        obj = json.loads(jsonData)
        
        bm = Bookmark(owner=user, title=obj["title"], url=obj["url"],
            valid_url=obj["valid_url"]
        )
        
        bm.save()
        
        if "added" in obj:
            bm.added = make_aware(datetime.strptime(obj["added"], _DT_FORMAT), UTC())
        
        for t in obj["tags"]:
            if isinstance(t, six.string_types):
                bm.tag(t)
            else:
                bm.tag(t["id"])
        
        bm.save()
        
        return bm
    
    def autotag_rules(self):
        """ Loops through all the autotag instances, and applies them
        
        Basically, loops through them all and if their pattern matches, it applies all the tags.
        """
        #TODO: Should see if I should do this in the database
        url = self.url.lower()
        for at in Autotag.by_user(self.owner):
            if at.pattern.lower() in url:
                for t in at.tags.all():
                    self.tag(t)
    
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
