""" Contains a few template tags relating to autotags

Specifically, the autotag tag itself, and the filters epoch and cstag.
"""

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from tags.models import Tag

import datetime
import calendar
import types

register = template.Library()

@register.inclusion_tag("autotags/autotag.html")
def autotag(autotag, untag=None, **kwargs):
    """ Displays an autotag as a block 
    
    An autotag block is a HTML element with the class "block", surprisingly enough, and consists of a head and a body.
    The head is always visible, but the body is only visible when you click the button, and contains buttons to edit the
    autotag.
    """
    kwargs["at"] = autotag
    kwargs["tags"] = Tag.expand_implies_check(autotag.tags.all())
    
    kwargs["colour"] = "white"
    for (t, _) in kwargs["tags"]:
        if t.colour != "white":
            kwargs["colour"] = t.colour
            break
    
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
