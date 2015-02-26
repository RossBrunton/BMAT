""" Context processors, these get called and add things to template contexts """
from django.conf import settings

from users.models import Settings

def theme(request):
    """ Adds the "theme" property to the context for the user's theme """
    if request.user.is_authenticated():
        return {"theme":request.user.settings.theme}
    else:
        return {"theme":Settings.THEME_LIGHT}
