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
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["tags"] = Tag.by_user(request.user)
    ctx["atf"] = AddTagForm({"type":"tag"})
    ctx["rtf"] = RemoveTagForm({"type":"tag"})
    
    return TemplateResponse(request, "tags/index.html", ctx)


@login_required
def filter(request, tag):
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
    tags = Tag.objects.filter(owner=request.user, slug__startswith=defaultfilters.slugify(value))[:10]
    
    return TemplateResponse(request, "tags/suggest.json", {"tags":tags, "value":value}, "application/json")


@login_required
@require_POST
def tag(request):
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
    tag = get_object_or_404(Tag, pk=tag, owner=request.user)
    
    return TemplateResponse(
        request, "tags/tagBlock.html",
        tagBlock(tag, AddTagForm({"type":"tag"}), RemoveTagForm({"type":"tag"}))
    )


@login_required
@require_POST
def rename(request, tag):
    
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
