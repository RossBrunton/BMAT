""" URLs for autotag related things

URLs are:
- home
- add
- delete
- (autotag)/html
- (autotag)/setPattern

"""

from django.conf.urls import url
import autotags.views as views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete$', views.delete, name="delete"),
    url(r'^create$', views.create, name="create"),
    url(r'^check$', views.check, name="check"),
    
    url(r'^(?P<autotag>[0-9]+)/html$', views.html, name="html"),
    url(r'^(?P<autotag>[0-9]+)/setPattern$', views.setPattern, name="setPattern"),
]
