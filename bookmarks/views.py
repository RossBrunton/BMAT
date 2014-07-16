from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import defaultfilters
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from bmat.utils import parse_split
from bookmarks.forms import AddTagForm
from bookmarks.models import bookmarks_by_user, Bookmark
from tags.models import Tag

@login_required
def home(request):
    start, end = parse_split(request.GET, "r", 0, 30)
    
    ctx = {}
    
    bms = bookmarks_by_user(request.user)
    ctx["area"] = "bookmarks"
    ctx["bookmarks"] = bms[start:end]
    ctx["atf"] = AddTagForm(auto_id=False)
    ctx["start"] = start
    ctx["end"] = end
    ctx["count"] = len(bms)
    
    return TemplateResponse(request, "bookmarks/index.html", ctx)


@login_required
def export(request):
    ctx = {}
    
    ctx["bookmarks"] = bookmarks_by_user(request.user)
    
    return TemplateResponse(request, "bookmarks/export.html", ctx)


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
            return HttpResponse('{"error":"Invalid URL"}', content_type="application/json", status=422)
    
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
    
    ctx = {}
    
    ctx["bm"] = bm
    ctx["tags"] = Tag.expand_implies(bm.tags.all())
    ctx["atf"] = AddTagForm(auto_id=False)
    
    return TemplateResponse(request, "bookmarks/bookmark.html", ctx)


@login_required
@require_POST
def tag(request, bookmark):
    f = AddTagForm(request.POST)
    
    try:
        bm = get_object_or_404(Bookmark, owner=request.user, pk=bookmark)
    except Bookmark.DoesNotExist:
        return HttpResponse('{"error":"Bookmark not found"}', content_type="application/json", status=422)
    
    if not f.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
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
def untag(request, bookmark):
    if "tag" not in request.POST:
        raise SuspiciousOperation
    
    bm = get_object_or_404(Bookmark, owner=request.user, pk=bookmark)
    
    try:
        tag = Tag.objects.get(owner=request.user, slug=request.POST["tag"])
    except Tag.DoesNotExist:
        return HttpResponse(
            '{"error":"Tag not found, maybe it\'s not on this bookmark, but implied from another one"}',
            content_type="application/json", status=422
        )
    
    bm.tags.remove(tag)
    
    return HttpResponse('{"bookmark":'+bm.to_json()+'}', content_type="application/json")


@login_required
@require_POST
def rename(request, bookmark):
    if "name" not in request.POST:
        raise SuspiciousOperation
    
    try:
        bm = Bookmark.objects.get(owner=request.user, pk=bookmark)
    except Bookmark.DoesNotExist:
        return HttpResponse('{"error":"Bookmark not found"}', content_type="application/json", status=422)
    
    bm.title = request.POST["name"]
    bm.save()
    
    return HttpResponse('{"bookmark":'+bm.to_json()+'}', content_type="application/json")
