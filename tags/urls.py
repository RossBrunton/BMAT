from django.conf.urls import patterns, include, url

import tags.views as views

urlpatterns = patterns("",
    url(r'^suggest/(?P<value>.*)$', "tags.views.suggest", name="suggest"),
)
