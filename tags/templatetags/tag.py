from django import template
from tags.models import Tag

register = template.Library()

@register.inclusion_tag('tags/tag.html', takes_context=True)
def tag(context, tag, obj, rtf, **kwargs):
    if isinstance(tag, Tag): 
        kwargs["tag"] = tag
        kwargs["explicit"] = False
    else:
        kwargs["tag"] = tag[0]
        kwargs["explicit"] = tag[1]
    
    kwargs["bookmark"] = obj
    kwargs["rtf"] = rtf
    kwargs["pk_target"] = obj.pk
    
    return kwargs

@register.inclusion_tag('tags/tagBlock.html', takes_context=True)
def tagBlock(context, tag, atf, rtf, **kwargs):
    kwargs["tag"] = tag
    kwargs["implies"] = Tag.expand_implies_check(tag.tags.all())
    kwargs["atf"] = atf
    kwargs["rtf"] = rtf
    
    return kwargs
