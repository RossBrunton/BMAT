from django.conf.urls import patterns, include, url
from django.contrib import admin

import bmat.views, bookmarks.urls, users.urls, tags.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', bmat.views.home, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^users/', include(users.urls, namespace="users")),
    url(r'^bookmarks/', include(bookmarks.urls, namespace="bookmarks")),
    url(r'^tags/', include(tags.urls, namespace="tags")),
)
