from django.conf.urls import patterns, include, url

import bookmarks.views as views

urlpatterns = patterns("",
    url(r'^$', "bookmarks.views.home", name="home"),
)
