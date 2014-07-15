from django.contrib.auth import logout as alogout, login as alogin, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from bmat import settings
from bookmarks.models import Bookmark
from users.forms import ImportForm

import random
import string
import re, datetime

@login_required
def home(request):
    ctx = {}
    
    ctx["area"] = "user"
    ctx["importForm"] = ImportForm()
    
    return TemplateResponse(request, "users/index.html", ctx)


@require_POST
@login_required
def importFile(request):
    form = ImportForm(request.POST, request.FILES)
    
    if not form.is_valid():
        return HttpResponse('{"error":"Invalid form"}', content_type="application/json", status=422)
    
    if request.FILES["file"].multiple_chunks():
        return HttpResponse('{"error":"File too large"}', content_type="application/json", status=422)
    
    try:
        __handle_import(request.FILES["file"].read(), form.data.get("use_tags", False), request.user)
    except:
        return HttpResponse('{"error":"Invalid file"}', content_type="application/json", status=422)
    
    return HttpResponseRedirect("/")


@require_POST
@login_required
def logout(request):
    alogout(request)
    
    return HttpResponseRedirect("/")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            alogin(request, form.get_user())

            return HttpResponseRedirect("/")
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form,
        'can_register': settings.BMAT_ALLOW_REGISTER
    }
    
    return TemplateResponse(request, "users/login.html", context)


def register(request):
    if not settings.BMAT_ALLOW_REGISTER:
        return render(request, "users/no_register.html", {})
    
    if request.method == "GET":
        return render(request, "users/register.html", {"form":UserCreationForm()})
    
    elif request.method == "POST":
        f = UserCreationForm(data=request.POST)
        
        if not f.is_valid():
            return render(request, "users/register.html", {"form":f})
        
        u = f.save()
    
    return redirect("/")


def __handle_import(contents, use_tags, owner):
    lines = contents.split("\n")
    
    title = re.compile(r"<a.*?>(.+?)</a>", re.I)
    url = re.compile(r"""<a.*href=['"](.+?)['"]""", re.I)
    tags = re.compile(r"""<a.*?tags=["'](.+?)["']""", re.I)
    addTime = re.compile(r"""<a.*?add_date=["'](\d+?)["']""", re.I)
    
    for l in lines:
        if "<a" in l.lower() and "</a>" in l.lower():
            bookmark = {}
            
            bookmark["title"] = title.search(l)
            if not bookmark["title"]:
                continue
            bookmark["title"] = bookmark["title"].group(1)
            
            bookmark["url"] = url.search(l)
            if not bookmark["url"]:
                continue
            bookmark["url"] = bookmark["url"].group(1)
            
            bookmark["tags"] = [];
            if use_tags:
                result = tags.search(l)
                if result:
                    bookmark["tags"] = result.group(1).split(",")
            
            bookmark["added"] = addTime.search(l)
            if bookmark["added"]:
                bookmark["added"] = bookmark["added"].group(1)
            
            try:
                Bookmark.objects.get(owner=owner, url=bookmark["url"])
            except Bookmark.DoesNotExist:
                bm = Bookmark(owner=owner, url=bookmark["url"], title=bookmark["title"])
                
                bm.save()
                if bookmark["added"]:
                    bm.added = datetime.datetime.fromtimestamp(int(bookmark["added"]))
                
                for t in bookmark["tags"]:
                    bm.tag(t)
                
                bm.save()
