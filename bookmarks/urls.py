""" URLs for bookmark related things 

URLs are:
- home
- export (For exporting bookmarks to HTML that browsers can import)
- add
- delete
- (bookmark)/html
- (bookmark)/rename

"""

from django.urls import re_path

import bookmarks.views as views

app_name="bookmarks"
urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'^export$', views.export, name="export"),
    re_path(r'^add$', views.add, name="add"),
    re_path(r'^delete$', views.delete, name="delete"),
    re_path(r'^create$', views.create, name="create"),
    
    re_path(r'^(?P<bookmark>[0-9]+)/html$', views.html, name="html"),
    re_path(r'^(?P<bookmark>[0-9]+)/rename$', views.rename, name="rename"),
]
