""" Root URL config """

from django.conf.urls import patterns, include, url
from django.contrib import admin

import bmat.views, bookmarks.urls, users.urls, tags.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', bmat.views.home, name="home"),
    url(r'^privacy$', bmat.views.privacy, name="privacy"),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^user/', include(users.urls, namespace="user")),
    url(r'^bookmarks/', include(bookmarks.urls, namespace="bookmarks")),
    url(r'^tags/', include(tags.urls, namespace="tags")),
)
