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

urlpatterns = patterns("",
    url(r'^$', "bookmarks.views.home", name="home"),
    url(r'^export$', "bookmarks.views.export", name="export"),
    url(r'^add$', "bookmarks.views.add", name="add"),
    url(r'^delete$', "bookmarks.views.delete", name="delete"),
    
    url(r'^(?P<bookmark>[0-9]+)/html$', "bookmarks.views.html", name="html"),
    url(r'^(?P<bookmark>[0-9]+)/rename$', "bookmarks.views.rename", name="rename"),
)
