from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import defaultfilters
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from tags.forms import AddTagForm, RemoveTagForm
from bookmarks.models import Bookmark
from tags.models import Tag
from .templatetags.bookmark import bookmark as bookmarkTag

@login_required
def home(request):
    ctx = {}
    
    paginator = Paginator(Bookmark.by_user(request.user), 30)
    bookmarks = None
    try:
        bookmarks = paginator.page(request.GET.get("p", "1"))
    except PageNotAnInteger:
        bookmarks = paginator.page(1)
    except EmptyPage:
        bookmarks = paginator.page(paginator.num_pages)
    
    ctx["area"] = "bookmarks"
    ctx["bookmarks"] = bookmarks
    ctx["atf"] = AddTagForm({"type":"bookmark"})
    ctx["rtf"] = RemoveTagForm({"type":"bookmark"})
    
    return TemplateResponse(request, "bookmarks/index.html", ctx)


@login_required
def export(request):
    ctx = {}
    
    ctx["bookmarks"] = Bookmark.by_user(request.user)
    
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
    
    if "tag" in request.POST:
        bm.tag(request.POST["tag"])
    
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
    
    return HttpResponse('{"deleted":'+str(id)+', "obj":'+json+', "type":"bookmark"}', content_type="application/json")


@login_required
def html(request, bookmark):
    bm = get_object_or_404(Bookmark, pk=bookmark, owner=request.user)
    
    return TemplateResponse(
        request, "bookmarks/bookmark.html", 
        bookmarkTag(bm, AddTagForm({"type":"bookmark"}), RemoveTagForm({"type":"bookmark"}))
    )


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
    
    return HttpResponse('{"obj":'+bm.to_json()+', "type":"bookmark"}', content_type="application/json")
