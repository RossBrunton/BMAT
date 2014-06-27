from django import template

register = template.Library()

@register.inclusion_tag('tags/tag.html', takes_context=True)
def tag(context, tag, **kwargs):
    kwargs["tag"] = tag
    
    return kwargs
