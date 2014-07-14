from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from bookmarks.models import Bookmark
from tags.models import Tag

import types

register = template.Library()

@register.inclusion_tag('bookmarks/bookmark.html', takes_context=True)
def bookmark(context, bookmark, atf, **kwargs):
    kwargs["bm"] = bookmark
    kwargs["tags"] = Tag.expand_implies(bookmark.tags.all())
    kwargs["atf"] = atf
    
    return kwargs
