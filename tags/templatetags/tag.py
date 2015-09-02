""" This contains the templatetags used to display and manipulate tags """
from django import template
from tags.models import Tag
from tags.forms import AddTagForm, RemoveTagForm, RenameTagForm

register = template.Library()

@register.inclusion_tag("tags/tag.html")
def tag(tag, obj, **kwargs):
    """ Displays a single tag as for the head of other blocks
    
    Tag may be either a Tag model instance, or a (tag, direct) pair. direct is a boolean indicating whether the tag is
    directly on this taggable thing, or if it's from an implication of another tag. If and only if a tag is direct will
    an "untag" button be shown.
    
    obj is the taggable object that this tag is attached to.
    """
    if isinstance(tag, Tag): 
        kwargs["tag"] = tag
        kwargs["direct"] = False
    else:
        kwargs["tag"] = tag[0]
        kwargs["direct"] = tag[1]
    
    kwargs["rtf"] = RemoveTagForm({"type":obj.taggable_type})
    kwargs["pk_target"] = obj.pk
    
    return kwargs

@register.inclusion_tag("tags/tagBlock.html")
def tagBlock(tag, **kwargs):
    """ Displays a tag block, for the tag list page
    
    Takes a tag, AddTagForm and RemoveTagForm.
    """
    kwargs["tag"] = tag
    kwargs["implies"] = Tag.expand_implies_check(tag.tags.all())
    kwargs["renametf"] = RenameTagForm(instance=tag)
    
    return kwargs


@register.inclusion_tag("tags/addTag.html")
def addTag(type, pk, **kwargs):
    """ Displays the "add tag" field with its button
    
    This will automatically download suggestions for the tag based on previous tags.
    
    It requires the pk of the thing being tagged, and an AddTagForm.
    """
    kwargs["pk"] = pk
    kwargs["atf"] = AddTagForm({"type":type})
    
    return kwargs

@register.inclusion_tag("tags/multiTag.html")
def multiTag(type, tag=None, **kwargs):
    """ Displays the "multiple tag widget"
    """
    kwargs["tag"] = tag
    kwargs["type"] = type
    kwargs["atf"] = AddTagForm({"type":type})
    
    return kwargs

@register.inclusion_tag("tags/multiTagButton.html")
def multiTagButton(**kwargs):
    """ Displays the "multiple tag widget"'s button """
    return kwargs
