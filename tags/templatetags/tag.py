""" This contains the templatetags used to display and manipulate tags """
from django import template
from tags.models import Tag

register = template.Library()

@register.inclusion_tag("tags/tag.html")
def tag(tag, obj, rtf, **kwargs):
    """ Displays a single tag as for the head of other blocks
    
    Tag may be either a Tag model instance, or a (tag, direct) pair. direct is a boolean indicating whether the tag is
    directly on this taggable thing, or if it's from an implication of another tag. If and only if a tag is direct will
    an "untag" button be shown.
    
    obj is the taggable object that this tag is attached to, and rtf is a RemoveTagForm.
    """
    if isinstance(tag, Tag): 
        kwargs["tag"] = tag
        kwargs["direct"] = False
    else:
        kwargs["tag"] = tag[0]
        kwargs["direct"] = tag[1]
    
    kwargs["rtf"] = rtf
    kwargs["pk_target"] = obj.pk
    
    return kwargs

@register.inclusion_tag("tags/tagBlock.html")
def tagBlock(tag, atf, rtf, **kwargs):
    """ Displays a tag block, for the tag list page
    
    Takes a tag, AddTagForm and RemoveTagForm.
    """
    kwargs["tag"] = tag
    kwargs["implies"] = Tag.expand_implies_check(tag.tags.all())
    kwargs["atf"] = atf
    kwargs["rtf"] = rtf
    
    return kwargs


@register.inclusion_tag("tags/addTag.html")
def addTag(atf, pk, **kwargs):
    """ Displays the "add tag" field with its button
    
    This will automatically download suggestions for the tag based on previous tags.
    
    It requires the pk of the thing being tagged, and an AddTagForm.
    """
    kwargs["pk"] = pk
    kwargs["atf"] = atf
    
    return kwargs
