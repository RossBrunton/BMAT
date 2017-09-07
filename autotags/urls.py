""" URLs for autotag related things

URLs are:
- home
- add
- delete
- (autotag)/html
- (autotag)/setPattern

"""

from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r'^$', "autotags.views.home", name="home"),
    url(r'^add$', "autotags.views.add", name="add"),
    url(r'^delete$', "autotags.views.delete", name="delete"),
    url(r'^create$', "autotags.views.create", name="create"),
    
    url(r'^(?P<autotag>[0-9]+)/html$', "autotags.views.html", name="html"),
    url(r'^(?P<autotag>[0-9]+)/setPattern$', "autotags.views.setPattern", name="setPattern"),
)
