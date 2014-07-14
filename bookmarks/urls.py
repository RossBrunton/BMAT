from django.conf.urls import patterns, include, url

import bookmarks.views as views

urlpatterns = patterns("",
    url(r'^$', "bookmarks.views.home", name="home"),
    url(r'^export$', "bookmarks.views.export", name="export"),
    url(r'^add$', "bookmarks.views.add", name="add"),
    url(r'^delete$', "bookmarks.views.delete", name="delete"),
    
    url(r'^(?P<bookmark>[0-9]+)/html$', "bookmarks.views.html", name="html"),
    url(r'^(?P<bookmark>[0-9]+)/tag$', "bookmarks.views.tag", name="tag"),
    url(r'^(?P<bookmark>[0-9]+)/untag$', "bookmarks.views.untag", name="untag"),
    url(r'^(?P<bookmark>[0-9]+)/rename$', "bookmarks.views.rename", name="rename"),
)
