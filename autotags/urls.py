""" URLs for autotag related things

URLs are:
- home
- add
- delete
- (autotag)/html
- (autotag)/setPattern

"""

from django.urls import re_path
import autotags.views as views

app_name="autotags"
urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'^add$', views.add, name="add"),
    re_path(r'^delete$', views.delete, name="delete"),
    re_path(r'^create$', views.create, name="create"),
    re_path(r'^check$', views.check, name="check"),
    
    re_path(r'^(?P<autotag>[0-9]+)/html$', views.html, name="html"),
    re_path(r'^(?P<autotag>[0-9]+)/setPattern$', views.setPattern, name="setPattern"),
]
