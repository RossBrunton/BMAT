""" Contains a few template tags relating to bookmarks

Specifically, the bookmark tag itself, and the filters epoch and cstag.
"""

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from tags.models import Tag

import datetime
import calendar
import types

register = template.Library()

@register.inclusion_tag("bookmarks/bookmark.html")
def bookmark(bookmark, untag=None, **kwargs):
    """ Displays a bookmark as a block 
    
    A bookmark block is a HTML element with the class "block", surprisingly enough, and consist of a head and a body.
    The head is always visible, but the body is only visible when you click the button, and contains buttons to edit the
    bookmark.
    """
    kwargs["bm"] = bookmark
    kwargs["tags"] = Tag.expand_implies_check(bookmark.tags.all())
    
    return kwargs


@register.filter(expects_localtime=True)
def epoch(value):
    """ Convert datetime object into seconds from epoch """
    if isinstance(value, datetime.datetime):
        return int(calendar.timegm(value.timetuple()))
    return ''


@register.filter()
def cstag(value):
    """ Return the tags for this bookmark as a comma seperated list """
    return ",".join(map((lambda t: t.slug.replace(",", "")), Tag.expand_implies(value.tags.all())))
