""" Models relating to tags 

This also contains "colours_enum" which is a list of (css_class, colour_name) for each colour.
"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaultfilters

import tags

import json
import six

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
    """ Base class for taggable models; anything taggable must extend this """
    class Meta:
        abstract = True
    
    def tag(self, tag):
        """ Tags this object with a tag specified by a tag name, primary key or Tag model instance """
        if isinstance(tag, six.integer_types):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except Tag.DoesNotExist:
                #Handle this better?
                return
        
        if isinstance(tag, six.string_types):
            try:
                tag = Tag.objects.get(slug=defaultfilters.slugify(tag), owner=self.owner)
            except Tag.DoesNotExist:
                tag = Tag(owner=self.owner, name=tag)
                tag.save()
        
        tag.owner = self.owner
        tag.save()
        self.tags.add(tag)
    
    def untag(self, tag):
        """ Untags this object from a tag specified by a tag name, primary key or Tag model instance """
        if isinstance(tag, six.integer_types):
            try:
                tag = Tag.objects.get(pk=tag, owner=self.owner)
            except Tag.DoesNotExist:
                return
        
        if isinstance(tag, six.string_types):
            try:
                tag = Tag.objects.get(slug=defaultfilters.slugify(tag), owner=self.owner)
            except Tag.DoesNotExist:
                return
        
        self.tags.remove(tag)
    
    @classmethod
    def get_by_tag(cls, tag):
        """ Returns all the elements tagged with the given tag or any other tags it implies """
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
    """ A Tag, which may be used to categorize taggable things
    
    Contains:
    - owner:ForeignKey to User
    - name:TextField
    - colour:CharField with choices being the colours enum
    - slug:SlugField
    - tags:ManyToManyField with itself
    - pinned:Whether the tag is pinned or not
    
    Tags themselves can be tagged, conceptually "Crowns" being tagged "Hats" means "Crowns" implies "Hats". Anything
    tagged with "Crowns" will also be tagged "Hats". This is dynamic, so it is not possible to have a crown that is not
    a hat, and removing the "hat" tag from "crown" will remove the hat tag from everything tagged "crown".
    
    Tags are ordered alphabetically.
    
    The slug of a tag is also set automatically when it is saved.
    """
    class Meta:
        ordering = ["slug"]
    
    owner = models.ForeignKey(User)
    name = models.TextField(max_length=100)
    colour = models.CharField(max_length=20, choices=colours_enum, default='white')
    slug = models.SlugField()
    tags = models.ManyToManyField("self", related_name="tags_to", symmetrical=False, db_table="tags_tag_implies")
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return ("Tag '"+self.name+"' for "+self.owner.username).encode("ascii", "ignore").decode("ascii")
    
    def to_dir(self):
        """ Returns a dictionary representation of this tag
        
        The keys of the object are the field names, and the values are the respective values.
        """
        out = {}
        out["name"] = self.name
        out["colour"] = self.colour
        out["slug"] = self.slug
        out["id"] = self.pk
        out["tags"] = []
        
        for t in self.tags.all():
            out["tags"].append(t.pk)
        
        return out
    
    def to_json(self):
        """ Produces the JSON representation of this tag
        
        It's the JSON for the output of to_dir()
        """
        return json.dumps(self.to_dir())
    
    def undoable_json(self):
        out = {}
        
        out["tag"] = self.to_dir()
        
        out["tagged_objects"] = {}
        
        for k, v in tags.taggables().items():
            out["tagged_objects"][k] = list(map(lambda x: x.pk, v.objects.filter(tags__pk=self.pk)))
        
        return json.dumps(out)
    
    @staticmethod
    def from_undoable(jsonData, user):
        """ Given the undoable JSON representation of the tag, creates one for it
        
        Note that this SAVES the object to the database.
        """
        obj = json.loads(jsonData)
        
        tag = Tag(owner=user, name=obj["tag"]["name"], colour=obj["tag"]["colour"],
            slug=obj["tag"]["slug"],
        )
        
        tag.save()
        
        for t in obj["tag"]["tags"]:
            tag.tag(t)
        
        for t, v in obj["tagged_objects"].items():
            taggable = tags.lookup_taggable(t)
            
            for pk in v:
                try:
                    taggable.objects.get(pk=pk).tag(tag.pk)
                except taggable.DoesNotExist:
                    pass
            
        
        tag.save()
        
        return tag
    
    
    @staticmethod
    def get_or_create_with_slug(owner, instance):
        """ Checks if a tag exists for a given user, and returns it if it does
        
        If it doesn't, the owner of the instance is set to the provided one, it is saved and then returned.
        """
        try:
            return Tag.objects.get(owner=owner, slug=defaultfilters.slugify(instance.name))
        except Tag.DoesNotExist:
            instance.owner = owner
            instance.save()
            return instance
    
    @staticmethod
    def expand_implies(tags):
        """ Takes an iterable of tags, and returns a list of those tags and all that they imply
        
        That is, make a list out of the argument, and for each tag T, add all T's tags to this list if they aren't in it
        already.
        
        The list is sorted alphabetically.
        
        For example, if A is tagged B (A implies B), then expand_implies([A]) == [A, B] and expand_implies([B]) == [B]
        """
        out = list(tags)
        
        i = 0
        while i < len(out):
            for implied in out[i].tags.all():
                if implied not in out:
                    out.append(implied)
            
            i += 1
        
        out.sort(key=lambda a: a.slug)
        return out
    
    @staticmethod
    def expand_implies_check(tags):
        """ Does the same as expand_implies, but each element is a (tag, direct) pair
        
        Direct is true only for the tags in the input iterable, not for the implied ones.
        """
        out = list(map(lambda x : (x, True), list(tags)))
        tlist = list(tags)
        
        i = 0
        while i < len(tlist):
            for implied in tlist[i].tags.all():
                if implied not in tlist:
                    out.append((implied, False))
                    tlist.append(implied)
            
            i += 1
        
        out.sort(key=lambda a: a[0].slug)
        return out
    
    @staticmethod
    def expand_implied_by(tags):
        """ Takes an iterable of tags, and returns a list of those tags and all that imply them
        
        That is, make a list out of the argument, and for each tag T, add all tags that have T as a tag if it isn't
        already in the list.
        
        The list is sorted alphabetically.
        
        For example if A is tagged B (A implies B), expand_implied_by([A]) == [A] and expand_implied_by([B]) == [A, B]
        """
        out = list(tags)
        
        i = 0
        while i < len(out):
            for implies in out[i].tags_to.all():
                if implies not in out:
                    out.append(implies)
            
            i += 1
        
        out.sort(key=lambda a: a.slug)
        return out
    
    @staticmethod
    def expand_implied_by_check(tags):
        """ Does the same as expand_implied_by, but each element is a (tag, direct) pair
        
        Direct is true only for the tags in the input iterable, not for the implied ones.
        """
        out = list(map(lambda x : (x, True), list(tags)))
        tlist = list(tags)
        
        i = 0
        while i < len(tlist):
            for implies in tlist[i].tags_to.all():
                if implies not in out:
                    out.append((implies, False))
                    tlist.append(implies)
            
            i += 1
        
        out.sort(key=lambda a: a[0].slug)
        return out

    @staticmethod
    def by_user(user):
        """ Returns all the tags owned by this user """
        return Tag.objects.all().filter(owner=user)


@receiver(post_save, sender=Tag)
def tag_save(sender, instance, created, **kwargs):
    """ Save hook, used to update the slug if it needs to be changed """
    if instance.slug != defaultfilters.slugify(instance.name):
        instance.slug = defaultfilters.slugify(instance.name)
        instance.save()
