from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import settings
import bookmarks.views

@login_required
def home(request):
    return redirect(reverse("bookmarks:home"))
