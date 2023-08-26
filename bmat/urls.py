""" Root URL config """

from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin

import bmat.views, bookmarks.urls, users.urls, tags.urls, search.urls, autotags.urls

admin.autodiscover()

urlpatterns = [
    url(r'^$', bmat.views.home, name="home"),
    url(r'^privacy$', bmat.views.privacy, name="privacy"),
    path(r"admin/", admin.site.urls),
    
    url(r'^user/', include("users.urls")),
    url(r'^bookmarks/', include("bookmarks.urls")),
    url(r'^autotags/', include("autotags.urls")),
    url(r'^tags/', include("tags.urls")),
    url(r'^search/', include("search.urls")),
]
