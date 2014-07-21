from django import template

register = template.Library()

@register.inclusion_tag('url_add.html')
def url_add(tag=None, **kwargs):
    if tag:
        tag = tag.slug
    kwargs["tag"] = tag
    
    return kwargs
