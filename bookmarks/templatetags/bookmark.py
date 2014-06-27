from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from bookmarks.models import Bookmark

import types

register = template.Library()

@register.inclusion_tag('bookmarks/bookmark.html', takes_context=True)
def bookmark(context, bookmark, **kwargs):
    kwargs["bm"] = bookmark
    kwargs["tags"] = bookmark.tags.all()
    
    return kwargs
