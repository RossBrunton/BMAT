from django.shortcuts import render, get_object_or_404, redirect
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
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

import random
import string
from bmat import settings

#@require_POST
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
