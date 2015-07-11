""" This module manages both tags, and methods for manipulating taggable things

A tag is associated with a "thing", which at the moment are only bookmarks and other tags. The list of tags something
has been associated with is stored on the "tags" field of that things model. For a thing to be taggable, it must
have this tags field, be decorated with the "taggable" decorator (with a name), and be a subclass of the Taggable model.

A distinction should be made between "tags" themselves, and "tag blocks". Tag blocks are the blocks that are displayed
on the "Tags" page (similar to bookmarks). If it doesn't mention "blocks", then it probably manipulates the tag elements
that are in the head of other blocks (i.e. On a bookmark, each tag displayed next to the menu button).
"""
from django.template import defaultfilters

_taggable = {}

def lookup_taggable(name):
    """ Given a name, gets the taggable model with that name """
    return _taggable.get(name, None)


def taggable(name):
    """ A decorator that makes the object taggable under the given name
    
    lookup_taggable, when given the name, will return the decorated model, and views and similar will use the type to
    determine which model to manipulate tags on.
    """
    def decorator(c):
        if not hasattr(c, "tags"):
            raise RuntimeError("Class {} does not have a tags property, but is taggable".format(c))
        
        _taggable[name] = c
        
        return c
    return decorator

def taggables():
    """ Returns an object, key is taggable name, value is taggable class """
    return _taggable
