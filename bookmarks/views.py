""" View functions for bookmarks """

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
from .forms import RenameBookmarkForm
from bookmarks.models import Bookmark
from tags.models import Tag
from .templatetags.bookmark import bookmark as bookmarkTag

@login_required
def home(request):
    """ Home page is a list of all bookmarks and uses template index.html """
    ctx = {}
    
    # Use the paginator
    paginator = Paginator(Bookmark.by_user(request.user), 30)
    bookmarks = None
    try:
        bookmarks = paginator.page(request.GET.get("p", "1"))
    except PageNotAnInteger:
        bookmarks = paginator.page(1)
    except EmptyPage:
        bookmarks = paginator.page(paginator.num_pages)
    
    # Set up the context
    ctx["area"] = "bookmarks"
    ctx["bookmarks"] = bookmarks
    ctx["atf"] = AddTagForm({"type":"bookmark"})
    ctx["rtf"] = RemoveTagForm({"type":"bookmark"})
    
    return TemplateResponse(request, "bookmarks/index.html", ctx)


@login_required
def export(request):
    """ This uses export.html to export the bookmarks into a format that can be imported by other systems """
    ctx = {}
    
    ctx["bookmarks"] = Bookmark.by_user(request.user)
    
    return TemplateResponse(request, "bookmarks/export.html", ctx)


@login_required
@require_POST
def add(request):
    """ Adds a new bookmark
    
    Expects the url to be provided by the url POST value.
    
    The URL is automatically validated, if it isn't a valid URL, then http:// is prepended to it. If that fails, then
    the bookmark isn't added and an error is sent.
    
    The title for the bookmark is automatically downloaded based on the URL.
    
    If it succeeds, it returns the JSON representation of thebookmark it has added.
    
    If it fails it returns a JSON object with only an "error" property.
    """
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
    """ Deletes the given bookmark
    
    This returns a JSON object with the following properties:
    deleted: The primary key of the deleted bookmark, or null if it didn't exist.
    obj: The JSON representation of the deleted bookmark, or null if it didn't exist.
    alreadyDeleted: True if and only if the bookmark was deleted before this request.
    type: Always "bookmark".
    
    If it encounters an error, the deleted property is null, and the other two are not specified.
    """
    if "bookmark" not in request.POST:
        raise SuspiciousOperation
    
    try:
        bm = Bookmark.objects.get(owner=request.user, pk=request.POST["bookmark"])
    except Bookmark.DoesNotExist:
        return HttpResponse(
            '{"obj":null, "type":"bookmark", "deleted":null, "alreadyDeleted":true}', content_type="application/json"
        )
    
    id = bm.pk
    json = bm.to_json()
    bm.delete()
    
    return HttpResponse(
        '{"deleted":'+str(id)+', "obj":'+json+', "type":"bookmark", "alreadyDeleted":false}',
        content_type="application/json"
    )


@login_required
def html(request, bookmark):
    """ Returns the bookmark's HTML block (what it looks like on the page)
    
    This uses the templatetag bookmarkTag to render the provided bookmark.
    """
    bm = get_object_or_404(Bookmark, pk=bookmark, owner=request.user)
    
    return TemplateResponse(
        request, "bookmarks/bookmark.html", 
        bookmarkTag(bm, AddTagForm({"type":"bookmark"}), RemoveTagForm({"type":"bookmark"}))
    )


@login_required
@require_POST
def rename(request, bookmark):
    """ Renames the given bookmark
    
    Expects "name" to be provided in the POST data.
    
    If it succeeds it returns a JSON object with "obj" being the JSON representation of the bookmark, and "type" which
    is always "bookmark".
    
    If it fails, it returns a JSON object with only an "error" proprerty.
    """
    bmObj = get_object_or_404(Bookmark, owner=request.user, pk=bookmark)
    
    form = RenameBookmarkForm(request.user, request.POST, instance=bmObj)
    
    if not form.is_valid():
        e = list(form.errors.keys())[0]+": "+list(form.errors.values())[0][0]
        return HttpResponse('{"error":"'+e+'"}', content_type="application/json", status=422)
    
    form.save()
    
    return HttpResponse('{"obj":'+bmObj.to_json()+', "type":"bookmark"}', content_type="application/json")
