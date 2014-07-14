from django import template

register = template.Library()

@register.inclusion_tag('tags/tag.html', takes_context=True)
def tag(context, tag, **kwargs):
    kwargs["tag"] = tag
    
    return kwargs

@register.inclusion_tag('tags/tagBlock.html', takes_context=True)
def tagBlock(context, tag, atf, **kwargs):
    kwargs["tag"] = tag
    kwargs["implies"] = tag.implies.all()
    kwargs["atf"] = atf
    
    return kwargs
