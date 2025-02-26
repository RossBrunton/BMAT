""" Root URL config """

from django.conf.urls import include
from django.urls import path, re_path
from django.contrib import admin

import bmat.views, bookmarks.urls, users.urls, tags.urls, search.urls, autotags.urls

admin.autodiscover()

urlpatterns = [
    re_path(r'^$', bmat.views.home, name="home"),
    re_path(r'^privacy$', bmat.views.privacy, name="privacy"),
    path(r"admin/", admin.site.urls),
    
    re_path(r'^user/', include("users.urls")),
    re_path(r'^bookmarks/', include("bookmarks.urls")),
    re_path(r'^autotags/', include("autotags.urls")),
    re_path(r'^tags/', include("tags.urls")),
    re_path(r'^search/', include("search.urls")),
]
