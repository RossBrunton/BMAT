from django import template

register = template.Library()

@register.inclusion_tag('pages.html')
def pages(page, url="", **kwargs):
    return {"pages":page.paginator, "current":page, "url":url}
