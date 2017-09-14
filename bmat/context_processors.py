"""Context processors, these get called and add things to template contexts"""
from django.conf import settings

def analytics_and_ads(request):
    """ Adds the google analytics code to the context """
    out = {}
    
    if request.user.is_authenticated() and request.user.settings.no_analytics:
        out["analytics_code"] = ""
    else:
        out["analytics_code"] = settings.ANALYTICS_CODE
    
    if request.user.is_authenticated() and request.user.settings.no_ads:
        out["ad_client"] = ""
    else:
        out["ad_client"] = settings.AD_CLIENT
        out["ad_slot_top"] = settings.AD_SLOT_TOP
        out["ad_slot_bottom"] = settings.AD_SLOT_BOTTOM
    
    return out

def add_webstore_url(request):
    return {"webstore_url":settings.CHROME_EXTENSION_WEBSTORE}
