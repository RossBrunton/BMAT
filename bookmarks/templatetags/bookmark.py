from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from tags.models import Tag

import datetime
import calendar
import types

register = template.Library()

@register.inclusion_tag('bookmarks/bookmark.html', takes_context=True)
def bookmark(context, bookmark, atf, rtf, untag=None, **kwargs):
    kwargs["bm"] = bookmark
    kwargs["tags"] = Tag.expand_implies_check(bookmark.tags.all())
    kwargs["atf"] = atf
    kwargs["rtf"] = rtf
    
    return kwargs


@register.filter(expects_localtime=True)
def epoch(value):
    """Convert datetime object into seconds from epoch"""
    if isinstance(value, datetime.datetime):
        return int(calendar.timegm(value.timetuple()))
    return ''


@register.filter()
def cstag(value):
    return ",".join(map((lambda t: t.slug.replace(",", "")), Tag.expand_implies(value.tags.all())))
