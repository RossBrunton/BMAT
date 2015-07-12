""" General views

At the moment this only contains the home page and the privacy policy.
"""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse

@login_required
def home(request):
    """ Home page is a redirect to the bookmarks list"""
    return redirect(reverse("bookmarks:home"))


def privacy(request):
    """ Privacy policy, uses bmat/privacy.html """
    return TemplateResponse(request, "bmat/privacy.html", {})
