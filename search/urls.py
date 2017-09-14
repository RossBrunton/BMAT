""" URLs for searching

URLs are:
- home
- results (for the AJAX stuff)

"""

from django.conf.urls import patterns, url
import search.views as views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^results$', views.results, name="results"),
]
