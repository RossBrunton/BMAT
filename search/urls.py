""" URLs for searching

URLs are:
- home
- results (for the AJAX stuff)

"""

from django.urls import re_path
import search.views as views

app_name="search"
urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'^results$', views.results, name="results"),
]
