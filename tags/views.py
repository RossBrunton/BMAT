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

from collections import OrderedDict
from tags.models import tags_by_user, Tag
from bookmarks.forms import AddTagForm

@login_required
def home(request):
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["tags"] = tags_by_user(request.user)
    ctx["atf"] = AddTagForm(auto_id=False)
    
    return TemplateResponse(request, "tags/index.html", ctx)


@login_required
def filter(request, tag):
    tag = get_object_or_404(Tag, owner=request.user, slug=defaultfilters.slugify(tag))
    
    ctx = {}
    
    ctx["area"] = "tags"
    ctx["bookmarks"] = tag.all_bookmarks()
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
    
    return TemplateResponse(request, "tags/tagBlock.html", {"tag":tag, "atf":AddTagForm(auto_id=False)})


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
    
    implicatee = Tag.get_if_exists(request.user, f.instance)
    implicatee.owner = request.user
    
    implicator.implies.add(implicatee)
    
    return HttpResponse('{"tag":'+implicator.to_json()+'}', content_type="application/json")
