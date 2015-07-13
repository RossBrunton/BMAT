""" View functions for user management """

from django.contrib.auth import logout as alogout, login as alogin, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.forms.util import ErrorList

from django.conf import settings
from bookmarks.models import Bookmark
from users.forms import ImportForm, CustomUserCreationForm, SettingsForm
from users import clean_trial

import random
import string
import re, datetime

@login_required
def home(request, note=""):
    """ The settings page for users
    
    If you post a SettingsForm to this, it will be saved. In all cases, it renders index.html to provide the user some
    account managment things.
    
    This view may also take a note, in which case the note will be displayed at the top of the page and the request
    will run as if it were a GET.
    """
    if request.method == "POST" and not note:
        form = SettingsForm(request.POST, instance=request.user.settings)
        if form.is_valid():
            form.save()
        
    else:
        form = SettingsForm(instance=request.user.settings)
    
    ctx = {}
    
    ctx["area"] = "user"
    ctx["importForm"] = ImportForm()
    ctx["pass_form"] = PasswordChangeForm(request.user)
    ctx["settings_form"] = form
    ctx["note"] = note
    
    return TemplateResponse(request, "users/index.html", ctx)


@login_required
def pass_change(request):
    """ The password change page
    
    If you pass it a Django PasswordChangeForm, it will save it, and display a message. If it fails, it renders the
    users home page.
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return home(request, "Password Changed Successfully")
    
    else:
        form = PasswordChangeForm(instance=request.user.settings)
    
    ctx = {}
    
    ctx["area"] = "user"
    ctx["importForm"] = ImportForm()
    ctx["pass_form"] = form
    ctx["settings_form"] = SettingsForm(instance=request.user.settings)
    
    return TemplateResponse(request, "users/index.html", ctx)


@require_POST
@login_required
def importFile(request):
    """ When sent an ImportForm, will import the bookmarks from the file
    
    Outputs the users/index.html on error with the appropriate form. If it succeeds, it redirects to the home page. This
    behaviour should probably be changed at some point.
    """
    
    form = ImportForm(request.POST, request.FILES)
    
    error = False
    
    def add_error(message):
        error_list = form._errors.setdefault("file", ErrorList())
        error_list.append(message)
    
    if not form.is_valid():
        error = True
    
    if not error and request.FILES["file"].multiple_chunks():
        add_error("File too large")
        error = True
    
    if not error:
        try:
            _handle_import(request.FILES["file"].read(), form.data.get("use_tags", False), request.user)
        except:
            add_error("File is invalid or not of a supported format")
            error = True
    
    if error:
        ctx = {}
        ctx["area"] = "user"
        ctx["importForm"] = form
        ctx["pass_form"] = PasswordChangeForm(request.user)
        ctx["settings_form"] = SettingsForm(instance=request.user.settings)
        
        return TemplateResponse(request, "users/index.html", ctx, status=422)
    
    return HttpResponseRedirect("/")


@require_POST
@login_required
def logout(request):
    """ Logs the user out and redirects them to the home page """
    alogout(request)
    
    return HttpResponseRedirect("/")


def login(request):
    """ Either displays or handles a login request
    
    If an AuthenticationForm is posted, the user will be logged in and be redirect to the value of the "next" GET value
    if it exists, otherwise they will be redirected to the home page.
    
    If this page is requested via GET, it just displays a log in form.
    
    This also deletes any expired trial users, since I have no idea where else to put it.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            clean_trial()
            alogin(request, form.get_user())

            return HttpResponseRedirect(request.GET.get("next", "/"))
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form,
        'can_register': settings.BMAT_ALLOW_REGISTER
    }
    
    return TemplateResponse(request, "users/login.html", context)


def register(request):
    """ Either registers a new user, displays a registration form or tells the user that they can't register
    
    If the setting BMAT_ALLOW_REGISTER is false, then this renders the template no_register.html and does nothing with
    any POST data.
    
    This uses the register.html template if users are allowed to register.
    """
    if not settings.BMAT_ALLOW_REGISTER:
        return render(request, "users/no_register.html", {})
    
    if request.method == "GET":
        return render(request, "users/register.html", {"form":CustomUserCreationForm()})
    
    elif request.method == "POST":
        f = CustomUserCreationForm(data=request.POST)
        
        if not f.is_valid():
            return render(request, "users/register.html", {"form":f})
        
        u = f.save(commit=False)
        
        u.email = f.cleaned_data.get("email", "")
        u.save()
    
    return redirect("/")


def _handle_import(contents, use_tags, owner):
    """ Handles the import of a bookmarks file
    
    Loops through all links in the file and adds them as bookmarks. It then tags them if the file contains tags and
    "use_tags" is true.
    """
    lines = str(contents, encoding="utf8").split("\n")
    
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
