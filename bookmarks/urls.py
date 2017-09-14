""" URLs for bookmark related things 

URLs are:
- home
- export (For exporting bookmarks to HTML that browsers can import)
- add
- delete
- (bookmark)/html
- (bookmark)/rename

"""

from django.conf.urls import patterns, url

import bookmarks.views as views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^export$', views.export, name="export"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete$', views.delete, name="delete"),
    url(r'^create$', views.create, name="create"),
    
    url(r'^(?P<bookmark>[0-9]+)/html$', views.html, name="html"),
    url(r'^(?P<bookmark>[0-9]+)/rename$', views.rename, name="rename"),
]
