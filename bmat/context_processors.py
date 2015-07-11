"""Context processors, these get called and add things to template contexts"""
from django.conf import settings

def analytics_and_ads(request):
    """ Adds the google analytics code to the context """
    if request.user.is_authenticated() and request.user.settings.no_analytics:
        return {"analytics_code":""}
    else:
        return {"analytics_code":settings.ANALYTICS_CODE}
