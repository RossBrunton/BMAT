from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth import logout as alogout, login as alogin, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.template.response import TemplateResponse
from django.template import defaultfilters
from django.views.decorators.cache import cache_page
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string

from collections import OrderedDict

from bookmarks.models import bookmarks_by_user, Bookmark
from bookmarks.forms import AddTagForm
from tags.models import Tag

@login_required
def home(request):
    ctx = {}
    
    ctx["area"] = "bookmarks"
    ctx["bookmarks"] = bookmarks_by_user(request.user)
    ctx["atf"] = AddTagForm(auto_id=False)
    
    return TemplateResponse(request, "bookmarks/index.html", ctx)


@login_required
@require_POST
def add(request):
    if "url" not in request.POST:
        raise SuspiciousOperation
    
    url = request.POST["url"]
    val = URLValidator()
    
    try:
        val(url)
    except ValidationError:
        try:
            val("http://"+url)
            url = "http://"+url
        except ValidationError:
            return HttpResponse('{"error":"Invalid Url"}', content_type="application/json")
    
    bm = Bookmark(owner=request.user, url=url)
    bm.download_title()
    bm.save()
    
    return HttpResponse(bm.to_json(), content_type="application/json")


@login_required
@require_POST
def delete(request):
    if "bookmark" not in request.POST:
        raise SuspiciousOperation
    
    try:
        bm = Bookmark.objects.get(owner=request.user, pk=request.POST["bookmark"])
    except Bookmark.DoesNotExist:
        return HttpResponse('{"deleted":null, "alreadyDeleted":true}', content_type="application/json")
    
    id = bm.pk
    json = bm.to_json()
    bm.delete()
    
    return HttpResponse('{"deleted":'+str(id)+', "bookmark":'+json+'}', content_type="application/json")


@login_required
def html(request, bookmark):
    bm = get_object_or_404(Bookmark, pk=bookmark, owner=request.user)
    
    return TemplateResponse(request, "bookmarks/bookmark.html", {"bm":bm, "atf":AddTagForm(auto_id=False)})


@login_required
@require_POST
def tag(request, bookmark):
    f = AddTagForm(request.POST)
    
    try:
        bm = get_object_or_404(Bookmark, owner=request.user, pk=bookmark)
    except Bookmark.DoesNotExist:
        return HttpResponse('{"error":"Bookmark not found"}', content_type="application/json")
    
    if not f.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json")
    
    tag = f.instance
    try:
        tag = Tag.objects.get(owner=request.user, slug=defaultfilters.slugify(f.instance.name))
    except Tag.DoesNotExist:
       pass
    
    f.instance.owner = request.user
    bm.tag(tag)
    
    return HttpResponse('{"bookmark":'+bm.to_json()+'}', content_type="application/json")


@login_required
@require_POST
def rename(request, bookmark):
    if "name" not in request.POST:
        raise SuspiciousOperation
    
    try:
        bm = get_object_or_404(Bookmark, owner=request.user, pk=bookmark)
    except Bookmark.DoesNotExist:
        return HttpResponse('{"error":"Bookmark not found"}', content_type="application/json")
    
    bm.title = request.POST["name"]
    bm.save()
    
    return HttpResponse('{"bookmark":'+bm.to_json()+'}', content_type="application/json")
