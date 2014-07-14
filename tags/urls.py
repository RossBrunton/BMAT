from django.conf.urls import patterns, include, url

import tags.views as views

urlpatterns = patterns("",
     url(r'^$', "tags.views.home", name="home"),
    
    url(r'^suggest/(?P<value>.*)$', "tags.views.suggest", name="suggest"),
    url(r'^delete$', "tags.views.delete", name="delete"),
    url(r'^rename/(?P<tag>.*)$', "tags.views.rename", name="rename"),
    url(r'^htmlBlock/(?P<tag>.*)$', "tags.views.htmlBlock", name="htmlBlock"),
    url(r'^implies/(?P<tag>.*)$', "tags.views.implies", name="implies"),
    url(r'^~(?P<tag>.*)$', "tags.views.filter", name="filter"),
)
