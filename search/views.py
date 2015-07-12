""" View functions for search """

from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from django.template import defaultfilters
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from bookmarks.models import Bookmark
from tags.models import Tag
from users.models import Settings
from tags.forms import AddTagForm, RemoveTagForm

import json

def _search_context(query, user):
    if not query:
        return {"bookmarks":[], "tags":[], "query":"", "area":"search"}
    
    ctx = {"query":query, "area":"search"}
    
    ctx["bmatf"] = AddTagForm({"type":"bookmark"})
    ctx["bmrtf"] = RemoveTagForm({"type":"bookmark"})
    ctx["tagatf"] = AddTagForm({"type":"tag"})
    ctx["tagrtf"] = RemoveTagForm({"type":"tag"})
    
    ctx["bookmarks"] = Bookmark.by_user(user).filter(Q(title__icontains=query) | Q(url__icontains=query))
    ctx["tags"] = Tag.by_user(user).filter(name__icontains=query)
    
    return ctx
    

@login_required
def home(request):
    """ Home is a form for results, with them below if the "q" GET var exists """
    
    ctx = _search_context(request.GET.get("q", ""), request.user)
    
    return TemplateResponse(request, "search/index.html", ctx)


@login_required
def results(request):
    """ Returns the actual body of the search results, for AJAX stuff """
    
    ctx = _search_context(request.GET.get("q", ""), request.user)
    
    return TemplateResponse(request, "search/results.html", ctx)
