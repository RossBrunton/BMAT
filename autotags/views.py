""" View functions for autotags """

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
from .forms import AutotagSetPatternForm
from .models import Autotag
from tags.models import Tag
from .templatetags.autotag import autotag as autotagTag
from users.models import Settings
from bmat.utils import make_page

import json

@login_required
def home(request):
    """ Home page is a list of all autotag rules and uses template index.html """
    ctx = {}
    
    # Set up the context
    ctx["area"] = "autotag"
    ctx["autotags"] = make_page(Autotag.by_user(request.user), request.GET.get("p"))
    
    return TemplateResponse(request, "autotags/index.html", ctx)


@login_required
@require_POST
def add(request):
    """ Adds a new autotag rule
    
    If it succeeds, it returns the JSON representation of the autotag it has added.
    
    If it fails it returns a JSON object with only an "error" property.
    """
    if "pattern" not in request.POST:
        raise SuspiciousOperation
    
    pattern = request.POST["pattern"]
    
    at = Autotag(owner=request.user, pattern=pattern)
    
    at.save()
    
    if "tag" in request.POST:
        at.tag(request.POST["tag"])
    
    return HttpResponse(at.to_json(), content_type="application/json")


@login_required
@require_POST
def create(request):
    """ Given the json representation of an autotag, creates it
    
    The autotag must have been from "to_json", and must be the "obj" POST value.
    
    If it succeeds it returns a JSON object with "obj" being the JSON representation of the bookmark, "type" which
    is always "autotag" and "id" which is the id of the newly created autotag.
    """
    if "obj" not in request.POST:
        raise SuspiciousOperation
    
    try:
        at = Autotag.from_json(request.POST.get("obj"), request.user)
    except Exception:
        raise SuspiciousOperation
    
    out = {}
    out["type"] = "autotag"
    out["obj"] = at.to_json()
    out["id"] = at.pk
    
    return HttpResponse(json.dumps(out), content_type="application/json")


@login_required
@require_POST
def delete(request):
    """ Deletes the given autotag
    
    Accepts a singe POST parameter: `autotag`, which is the id of the rule to be deleted.
    
    This returns a JSON object with the following properties:
    deleted: The primary key of the deleted autotag, or null if it didn't exist.
    obj: The JSON representation of the deleted autotag, or null if it didn't exist.
    alreadyDeleted: True if and only if the autotag was deleted before this request.
    type: Always "autotag".
    
    If it encounters an error, the deleted property is null and alreadyDeleted is true
    """
    if "autotag" not in request.POST:
        raise SuspiciousOperation
    
    try:
        at = Autotag.objects.get(owner=request.user, pk=request.POST["autotag"])
    except Bookmark.DoesNotExist:
        return HttpResponse(
            '{"obj":null, "type":"autotag", "deleted":null, "alreadyDeleted":true}', content_type="application/json"
        )
    
    id = at.pk
    json = at.to_json()
    at.delete()
    
    return HttpResponse(
        '{"deleted":'+str(id)+', "obj":'+json+', "type":"autotag", "alreadyDeleted":false}',
        content_type="application/json"
    )


@login_required
def html(request, autotag):
    """ Returns the autotag's HTML block (what it looks like on the page)
    
    This uses the templatetag autotagTag to render the provided bookmark.
    """
    at = get_object_or_404(Autotag, pk=autotag, owner=request.user)
    
    return TemplateResponse(
        request, "autotags/autotag.html", 
        autotagTag(at)
    )


@login_required
@require_POST
def setPattern(request, autotag):
    """ Sets the pattern of the given autotag
    
    Expects "pattern" to be provided in the post data.
    
    If it succeeds it returns a JSON object with "obj" being the JSON representation of the autotag, and "type" which
    is always "autotag".
    
    If it fails, it returns a JSON object with only an "error" proprerty.
    """
    atObj = get_object_or_404(Autotag, owner=request.user, pk=autotag)
    
    form = AutotagSetPatternForm(request.POST, instance=atObj)
    
    if not form.is_valid():
        e = list(form.errors.keys())[0]+": "+list(form.errors.values())[0][0]
        return HttpResponse('{"error":"'+e+'"}', content_type="application/json", status=422)
    
    form.save()
    
    return HttpResponse('{"obj":'+atObj.to_json()+', "type":"autotag"}', content_type="application/json")
