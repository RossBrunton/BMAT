from django import template

register = template.Library()

@register.inclusion_tag('url_add.html')
def url_add(tag=None, **kwargs):
    """ Displays a box containing an "add page" entry box and its form
    
    If tag is specified, it is the slug of a tag which will be assigned to the URL when it is submitted.
    """
    if tag:
        tag = tag.slug
    kwargs["tag"] = tag
    
    return kwargs
