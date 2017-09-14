from django import template

register = template.Library()

@register.inclusion_tag('form_errors.html')
def form_errors(form):
    """ Displays errors on a form using the form_errors template"""
    return {"form":form}
