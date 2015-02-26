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

from tags.models import Tag
from tags.forms import AddTagForm, RemoveTagForm, RenameTagForm
import tags
from bookmarks.models import Bookmark
from .templatetags.tag import tagBlock

@login_required
def home(request):
    """ Uses index.html to display a list of all the user's tags """
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["tags"] = Tag.by_user(request.user)
    ctx["atf"] = AddTagForm({"type":"tag"})
    ctx["rtf"] = RemoveTagForm({"type":"tag"})
    
    return TemplateResponse(request, "tags/index.html", ctx)


@login_required
def filter(request, tag):
    """ Given a slug, uses filter.html to display all the things tagged with that specific tag """
    tag = get_object_or_404(Tag, owner=request.user, slug=defaultfilters.slugify(tag))
    
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["bookmarks"] = Bookmark.get_by_tag(tag)
    ctx["tag"] = tag
    ctx["atf"] = AddTagForm({"type":"tag"})
    ctx["rtf"] = RemoveTagForm({"type":"tag"})
    
    return TemplateResponse(request, "tags/filter.html", ctx)

@login_required
def suggest(request, value):
    """ Returns a JSON object containing tag suggestions for the sepecified value
    
    The JSON object contains two values:
    - yours: The string that was submitted to this page
    - tags: An array of strings for the suggestions
    """
    tags = Tag.objects.filter(owner=request.user, slug__startswith=defaultfilters.slugify(value))[:10]
    
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
        obj = get_object_or_404(taggable, owner=request.user, pk=f.cleaned_data["pk"])
    except taggable.DoesNotExist:
        return HttpResponse('{"error":"Taggable not found"}', content_type="application/json", status=422)
    
    tag = f.instance
    try:
        tag = Tag.objects.get(owner=request.user, slug=defaultfilters.slugify(f.instance.name))
    except Tag.DoesNotExist:
        pass
    
    f.instance.owner = request.user
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
    json = tag.to_json()
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
    
    return TemplateResponse(
        request, "tags/tagBlock.html",
        tagBlock(tag, AddTagForm({"type":"tag"}), RemoveTagForm({"type":"tag"}))
    )


@login_required
@require_POST
def rename(request, tag):
    """ Renames a tag using a RenameTagForm
    
    If successfull, outputs a JSON object with "obj" and "type" properties. "obj" is the JSON object of the tag that was
    renamed, while "type" will always be "tag".
    
    If it fails, a JSON object with an "error" value will be returned.
    """
    tagObj = get_object_or_404(Tag, owner=request.user, slug=tag)
    
    form = RenameTagForm(request.POST, instance=tagObj)
    
    if not form.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    try:
        existing = Tag.objects.get(owner=request.user, slug=defaultfilters.slugify(form.data["name"]))
        if existing.pk != form.instance.pk:
            return HttpResponse('{"error":"Tag already exists"}', content_type="application/json", status=422)
    except Tag.DoesNotExist:
        pass
    
    form.save()
    
    return HttpResponse('{"obj":'+tagObj.to_json()+', "type":"tag"}', content_type="application/json")
