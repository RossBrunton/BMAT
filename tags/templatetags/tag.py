from django import template
from tags.models import Tag

register = template.Library()

@register.inclusion_tag("tags/tag.html")
def tag(tag, obj, rtf, **kwargs):
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
    kwargs["tag"] = tag
    kwargs["implies"] = Tag.expand_implies_check(tag.tags.all())
    kwargs["atf"] = atf
    kwargs["rtf"] = rtf
    
    return kwargs


@register.inclusion_tag("tags/addTag.html")
def addTag(atf, pk, **kwargs):
    kwargs["pk"] = pk
    kwargs["atf"] = atf
    
    return kwargs
