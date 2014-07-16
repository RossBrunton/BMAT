from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

@login_required
def home(request):
    return redirect(reverse("bookmarks:home"))
