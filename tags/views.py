from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import defaultfilters
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from tags.models import Tag
from bookmarks.forms import AddTagForm
from bookmarks.models import Bookmark
from .templatetags.tag import tagBlock

@login_required
def home(request):
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["tags"] = Tag.by_user(request.user)
    ctx["atf"] = AddTagForm(auto_id=False)
    
    return TemplateResponse(request, "tags/index.html", ctx)


@login_required
def filter(request, tag):
    tag = get_object_or_404(Tag, owner=request.user, slug=defaultfilters.slugify(tag))
    
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["bookmarks"] = Bookmark.get_by_tag(tag)
    ctx["tag"] = tag
    ctx["atf"] = AddTagForm(auto_id=False)
    
    return TemplateResponse(request, "tags/filter.html", ctx)

@login_required
def suggest(request, value):
    tags = Tag.objects.filter(owner=request.user, slug__startswith=defaultfilters.slugify(value))[:10]
    
    return TemplateResponse(request, "tags/suggest.json", {"tags":tags, "value":value}, "application/json")


@login_required
@require_POST
def delete(request):
    if "tag" not in request.POST:
        raise SuspiciousOperation
    
    try:
        tag = Tag.objects.get(owner=request.user, pk=request.POST["tag"])
    except Tag.DoesNotExist:
        return HttpResponse('{"deleted":null, "alreadyDeleted":true}', content_type="application/json")
    
    id = tag.pk
    json = tag.to_json()
    tag.delete()
    
    return HttpResponse('{"deleted":'+str(id)+', "tag":'+json+'}', content_type="application/json")


@login_required
def htmlBlock(request, tag):
    tag = get_object_or_404(Tag, slug=tag, owner=request.user)
    
    return TemplateResponse(request, "tags/tagBlock.html", tagBlock({}, tag, AddTagForm(auto_id=False)))


@login_required
@require_POST
def rename(request, tag):
    
    tagObj = get_object_or_404(Tag, owner=request.user, slug=tag)
    
    form = AddTagForm(request.POST, instance=tagObj)
    
    if not form.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    try:
        existing = Tag.objects.get(owner=request.user, slug=defaultfilters.slugify(form.data["name"]))
        if existing.pk != form.instance.pk:
            return HttpResponse('{"error":"Tag already exists"}', content_type="application/json", status=422)
    except Tag.DoesNotExist:
        pass
    
    form.save()
    
    return HttpResponse('{"tag":'+tagObj.to_json()+'}', content_type="application/json")


@login_required
@require_POST
def implies(request, tag):
    f = AddTagForm(request.POST)
    
    try:
        implicator = get_object_or_404(Tag, owner=request.user, slug=tag)
    except Tag.DoesNotExist:
        return HttpResponse('{"error":"Tag not found"}', content_type="application/json", status=422)
    
    if not f.is_valid():
        return HttpResponse('{"error":"Form invalid"}', content_type="application/json", status=422)
    
    implicatee = Tag.get_or_create_with_slug(request.user, f.instance)
    implicatee.owner = request.user
    
    implicator.tags.add(implicatee)
    
    return HttpResponse('{"tag":'+implicator.to_json()+'}', content_type="application/json")


@login_required
@require_POST
def unimply(request, tag):
    if "tag" not in request.POST:
        raise SuspiciousOperation
    
    parent = get_object_or_404(Tag, owner=request.user, slug=tag)
    
    try:
        child = Tag.objects.get(owner=request.user, slug=request.POST["tag"])
    except Tag.DoesNotExist:
        return HttpResponse('{"error":"Tag not found"}', content_type="application/json", status=422)
    
    parent.tags.remove(child)
    
    return HttpResponse('{"tag":'+parent.to_json()+'}', content_type="application/json")
