""" General views

At the moment this only contains the home page and the privacy policy.
"""

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from users.views import login

def home(request):
    """ Home page is a redirect to the bookmarks list or a direct insert of the login page"""
    if request.user.is_authenticated:
        return redirect(reverse("bookmarks:home"))
    else:
        return login(request)


def privacy(request):
    """ Privacy policy, uses bmat/privacy.html """
    return TemplateResponse(request, "bmat/privacy.html", {})
