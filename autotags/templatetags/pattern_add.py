from django import template

register = template.Library()

@register.inclusion_tag('autotags/pattern_add.html')
def url_add(**kwargs):
    """ Displays a box containing an "add pattern" entry box and its form
    """
    
    return kwargs
