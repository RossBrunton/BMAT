""" View functions for tag related things

This includes both viewing the tag list, and manipulating tags on other things.
"""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import defaultfilters
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from tags.models import Tag
from tags.forms import AddTagForm, RemoveTagForm, RenameTagForm, PinTagForm
import tags
from tags import makeslug
from bookmarks.models import Bookmark
from .templatetags.tag import tagBlock
from bmat.utils import make_page

import json

@login_required
def home(request):
    """ Uses index.html to display a list of all the user's tags """
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["tags"] = make_page(Tag.by_user(request.user), request.GET.get("p"))
    ctx["untag_count"] = Bookmark.by_user(request.user).filter(tags=None).count()
    
    return TemplateResponse(request, "tags/index.html", ctx)


@login_required
def filter(request, tag):
    """ Given a slug, uses filter.html to display all the things tagged with that specific tag """
    tag = get_object_or_404(Tag, owner=request.user, slug=makeslug(tag))
    
    ctx = {}
    
    if not tag.pinned:
        # Don't display "tags" thing as active when the tag is pinned
        ctx["area"] = "tags"
    
    ctx["tag"] = tag
    ctx["pin_form"] = PinTagForm(instance=tag)
    ctx["bookmarks"] = make_page(Bookmark.get_by_tag(tag), request.GET.get("p"))
    
    return TemplateResponse(request, "tags/filter.html", ctx)

@login_required
def untagged(request):
    """ Given a slug, uses filter.html to display all the things tagged with that specific tag """
    
    ctx = {}
    bookmarks = Bookmark.by_user(request.user).filter(tags=None)
    ctx["untag_count"] = bookmarks.count()
    ctx["area"] = "tags"
    ctx["tag"] = None
    ctx["bookmarks"] = make_page(bookmarks, request.GET.get("p"))
    
    return TemplateResponse(request, "tags/filter.html", ctx)

@login_required
def suggest(request, value):
    """ Returns a JSON object containing tag suggestions for the sepecified value
    
    The JSON object contains two values:
    - yours: The string that was submitted to this page
    - tags: An array of strings for the suggestions
    """
    tags = Tag.objects.filter(owner=request.user, slug__startswith=makeslug(value))[:10]
    
    return TemplateResponse(request, "tags/suggest.json", {"tags":tags, "value":value}, "application/json")


@login_required
@require_POST
def tag(request):
    """ Tags a thing using an AddTagForm
    
    Returns a JSON response with an "obj" and "key" porperty. "obj" is the object that was tagged, while "type" is it's
    type. If there is an error, a JSON object with an "error" key is returned instead.
    """
    f = AddTagForm(request.POST)
    
    if not f.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    taggable = tags.lookup_taggable(f.cleaned_data["type"])
    
    if taggable is None:
        return HttpResponse('{"error":"Taggable type invalid"}', content_type="application/json", status=422)
    
    try:
        obj = taggable.objects.get(owner=request.user, pk=f.cleaned_data["pk"])
    except taggable.DoesNotExist:
        return HttpResponse('{"error":"Taggable not found"}', content_type="application/json", status=422)
    
    tag_names = map(lambda x: x.strip(), f.cleaned_data["name"].split(","))
    
    for n in tag_names:
        if not n:
            continue
        
        try:
            tag = Tag.objects.get(owner=request.user, slug=makeslug(n))
        except Tag.DoesNotExist:
            tag = Tag(owner=request.user, name=n, colour=f.instance.colour)
            tag.save()
        
        obj.tag(tag)
    
    return HttpResponse(
        '{{"obj":{}, "type":"{}"}}'.format(obj.to_json(), f.cleaned_data["type"]),
        content_type="application/json"
    )


@login_required
@require_POST
def untag(request):
    """ Untags a thing using a RemoveTagForm
    
    Returns a JSON response with a "deleted" and "key" porperty. "deleted" is the primary key of the object that had
    its tag removed, while "type" is it's type. If there is an error, a JSON object with an "error" key is returned
    instead.
    """
    f = RemoveTagForm(request.POST)
    
    if not f.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    taggable = tags.lookup_taggable(f.cleaned_data["type"])
    if taggable is None:
        return HttpResponse('{"error":"Taggable type invalid"}', content_type="application/json", status=422)
    
    try:
        obj = get_object_or_404(taggable, owner=request.user, pk=f.cleaned_data["target_pk"])
    except taggable.DoesNotExist:
        return HttpResponse('{"error":"Taggable not found"}', content_type="application/json", status=422)
    
    try:
        tag = Tag.objects.get(owner=request.user, pk=f.cleaned_data["tag_pk"])
    except Tag.DoesNotExist:
        return HttpResponse('{"error":"Tag to remove not found"}', content_type="application/json", status=422)
    
    obj.tags.remove(tag)
    
    return HttpResponse(
        '{{"deleted":{}, "type":"{}"}}'.format(obj.pk, f.cleaned_data["type"]), content_type="application/json"
    )


@login_required
@require_POST
def restore(request):
    """ Given the undoable json representation of a bookmark, performs the undo, recovering the tag
    
    The tag must have been from "undoable_json", and must be the "obj" POST value.
    
    If it succeeds it returns a JSON object with "obj" being the JSON representation of the bookmark, "type" which
    is always "tag" and "id" which is the id of the newly created bookmark.
    """
    if "obj" not in request.POST:
        raise SuspiciousOperation
    
    try:
        tag = Tag.from_undoable(request.POST.get("obj"), request.user)
    except Exception:
        raise SuspiciousOperation
    
    out = {}
    out["type"] = "tag"
    out["obj"] = tag.to_json()
    out["id"] = tag.pk
    
    return HttpResponse(json.dumps(out), content_type="application/json")


@login_required
@require_POST
def delete(request):
    """ Deletes a tag
    
    The primary key of the tag must be specified with the "tag" POST value. If the tag doesn't exist, nothing happens.
    
    This returns a JSON object with the following properties:
    deleted: The primary key of the deleted tag, or null if it didn't exist.
    obj: The JSON representation of the deleted tag, or null if it didn't exist.
    alreadyDeleted: True if and only if the tag was deleted before this request.
    type: Always "tag".
    """
    if "tag" not in request.POST:
        raise SuspiciousOperation
    
    try:
        tag = Tag.objects.get(owner=request.user, pk=request.POST["tag"])
    except Tag.DoesNotExist:
        return HttpResponse(
            '{"deleted":null, "obj":null, "alreadyDeleted":true, "type":"tag"}', content_type="application/json"
        )
    
    id = tag.pk
    json = tag.undoable_json()
    tag.delete()
    
    return HttpResponse(
        '{"deleted":'+str(id)+', "obj":'+json+', "alreadyDeleted":false, "type":"tag"}',
        content_type="application/json"
    )


@login_required
def htmlBlock(request, tag):
    """ Outputs the HTML for a tag block, such as for the tags list page
    
    This uses the tagBlock.html temlpate.
    """
    tag = get_object_or_404(Tag, pk=tag, owner=request.user)
    
    return TemplateResponse(request, "tags/tagBlock.html", tagBlock(tag))


@login_required
@require_POST
def rename(request, tag):
    """ Renames a tag using a RenameTagForm
    
    If successfull, outputs a JSON object with "obj", "type" and "pooled" properties. "obj" is the JSON object of the
    tag that was renamed, while "type" will always be "tag". pooled is true when the tag has been renamed to that of an
    existing tag, in which case "obj" will be that tag. 
    
    If it fails, a JSON object with an "error" value will be returned.
    """
    tagObj = get_object_or_404(Tag, owner=request.user, slug=tag)
    
    form = RenameTagForm(request.POST, instance=tagObj)
    
    if not form.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    if Tag.objects.filter(owner=request.user, slug=makeslug(form.data["name"])).exclude(pk=form.instance.pk).exists():
        # Tag exists, pool them
        existing = Tag.objects.get(owner=request.user, slug=makeslug(form.data["name"]))
        form.instance.pool_into(existing)
        form.instance.delete()
        tagObj = existing
        pooled = "true"
    else:
        form.save()
        pooled = "false"
    
    return HttpResponse('{"obj":'+tagObj.to_json()+', "type":"tag", "pooled":'+pooled+'}',
        content_type="application/json")


@login_required
@require_POST
def pin(request, tag):
    """ Updates a tags pinning using a PinTagForm
    
    If successfull, outputs a JSON object with "obj" and "type" properties. "obj" is the JSON object of the tag that was
    renamed, while "type" will always be "tag".
    
    If it fails, a JSON object with an "error" value will be returned.
    """
    tagObj = get_object_or_404(Tag, owner=request.user, slug=tag)
    
    form = PinTagForm(request.POST, instance=tagObj)
    
    if not form.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    form.save()
    
    return HttpResponse('{"obj":'+tagObj.to_json()+', "type":"tag"}', content_type="application/json")
