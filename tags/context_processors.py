"""Context processors, these get called and add things to template contexts"""
from .models import Tag

def pinned_tags(request):
    """ Adds the list of tags this user has pinned """
    out = {}
    
    if request.user.is_authenticated:
        out["pinned_tags"] = Tag.by_user(request.user).filter(pinned=True)
    
    return out
