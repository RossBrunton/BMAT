from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaultfilters

import tags

import json

colours_enum = [
    ("white", "White"),
    ("black", "Black"),
    ("darkblue", "Dark Blue"),
    ("darkgreen", "Dark Green"),
    ("darkred", "Dark Red"),
    ("blue", "Blue"),
    ("green", "Green"),
    ("red", "Red"),
    ("yellow", "Yellow"),
    ("magenta", "Magenta"),
    ("cyan", "Cyan"),
    ("orange", "Orange"),
]

class Taggable(models.Model):
    class Meta:
        abstract = True
    
    def tag(self, tag):
        if isinstance(tag, (int, long)):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except Tag.DoesNotExist:
                #Handle this better?
                return
        
        if isinstance(tag, (str, unicode)):
            try:
                tag = Tag.objects.get(slug=defaultfilters.slugify(tag), owner=self.owner)
            except Tag.DoesNotExist:
                tag = Tag(owner=self.owner, name=tag)
                tag.save()
        
        tag.owner = self.owner
        tag.save()
        self.tags.add(tag)
    
    def untag(self, tag):
        if isinstance(tag, (int, long)):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except Tag.DoesNotExist:
                return
        
        if type(tag) == str:
            try:
                tag = Tag.objects.get(name__iexact=tag, owner=self.owner)
            except Tag.DoesNotExist:
                return
        
        self.tags.remove(tag)
    
    @classmethod
    def get_by_tag(cls, tag):
        out = []
        
        tags = Tag.expand_implied_by([tag])
        
        for t in tags:
            results = cls.objects.filter(owner=tag.owner, tags=t)
            
            for b in results:
                if b not in out:
                    out.append(b)
        
        return out


@tags.taggable("tag")
class Tag(Taggable):
    class Meta:
        ordering = ["slug"]
    
    owner = models.ForeignKey(User)
    name = models.TextField(max_length=100)
    colour = models.CharField(max_length=20, choices=colours_enum, default='white')
    slug = models.SlugField()
    tags = models.ManyToManyField("self", related_name="tags_to", symmetrical=False, db_table="tags_tag_implies")

    def __str__(self):
        return ("Tag '"+self.name+"' for "+self.owner.username).encode("ascii", "ignore")
    
    def to_dir(self):
        out = {}
        out["name"] = self.name
        out["colour"] = self.colour
        out["slug"] = self.slug
        out["id"] = self.pk
        
        return out
    
    def to_json(self):
        return json.dumps(self.to_dir())
    
    @staticmethod
    def get_or_create_with_slug(owner, instance):
        try:
            return Tag.objects.get(owner=owner, slug=defaultfilters.slugify(instance.name))
        except Tag.DoesNotExist:
            instance.owner = owner
            instance.save()
            return instance
    
    @staticmethod
    def expand_implies(tags):
        out = list(tags)
        
        i = 0
        while i < len(out):
            for implied in out[i].tags.all():
                if implied not in out:
                    out.append(implied)
            
            i += 1
        
        out.sort(lambda a, b: cmp(a.slug, b.slug))
        return out
    
    @staticmethod
    def expand_implies_check(tags):
        """ Same as expand_implies, but as a pair, second element is whether the given tag is attached directly rather
        than implied. """
        out = map(lambda x : (x, True), list(tags))
        tlist = list(tags)
        
        i = 0
        while i < len(tlist):
            for implied in tlist[i].tags.all():
                if implied not in tlist:
                    out.append((implied, False))
                    tlist.append(implied)
            
            i += 1
        
        out.sort(lambda a, b: cmp(a[0].slug, b[0].slug))
        return out
    
    @staticmethod
    def expand_implied_by(tags):
        out = list(tags)
        
        i = 0
        while i < len(out):
            for implies in out[i].tags_to.all():
                if implies not in out:
                    out.append(implies)
            
            i += 1
        
        out.sort(lambda a, b: cmp(a.slug, b.slug))
        return out
    
    @staticmethod
    def expand_implied_by_check(tags):
        """ Same as expand_implied_by, but as a pair, second element is whether the given tag is attached directly
        rather than implied. """
        out = map(lambda x : (x, True), list(tags))
        tlist = list(tags)
        
        i = 0
        while i < len(tlist):
            for implies in tlist[i].tags_to.all():
                if implies not in out:
                    out.append((implies, False))
                    tlist.append(implies)
            
            i += 1
        
        out.sort(lambda a, b: cmp(a[0].slug, b[0].slug))
        return out

    @staticmethod
    def by_user(user):
        return Tag.objects.all().filter(owner=user)


@receiver(post_save, sender=Tag)
def tag_save(sender, instance, created, **kwargs):    
    if instance.slug != defaultfilters.slugify(instance.name):
        instance.slug = defaultfilters.slugify(instance.name)
        instance.save()
