""" General views

At the moment this only contains the home page.
"""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

@login_required
def home(request):
    """ Home page is a redirect to the bookmarks list"""
    return redirect(reverse("bookmarks:home"))
