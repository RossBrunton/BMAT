from django import template
from tags.models import Tag

register = template.Library()

@register.inclusion_tag('tags/tag.html', takes_context=True)
def tag(context, tag, bookmark=None, **kwargs):
    if isinstance(tag, Tag): 
        kwargs["tag"] = tag
        kwargs["explicit"] = False
    else:
        kwargs["tag"] = tag[0]
        kwargs["explicit"] = tag[1]
    
    kwargs["bookmark"] = bookmark
    
    return kwargs

@register.inclusion_tag('tags/tagBlock.html', takes_context=True)
def tagBlock(context, tag, atf, **kwargs):
    kwargs["tag"] = tag
    kwargs["implies"] = tag.implies.all()
    kwargs["atf"] = atf
    
    return kwargs
