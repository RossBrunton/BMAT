""" URLs for searching

URLs are:
- home
- results (for the AJAX stuff)

"""

from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r'^$', "search.views.home", name="home"),
    url(r'^results$', "search.views.results", name="results"),
)
