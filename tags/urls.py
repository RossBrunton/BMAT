""" URLs for tag related things 

URLs are:
- home
- suggest/(query)
- delete
- rename/(tag)
- htmlBlock/(tag)
- tag
- untag
- ~(tag) (named "filter")

"""

from django.urls import re_path
import tags.views as views

app_name="tags"
urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    
    re_path(r'^suggest/(?P<value>.*)$', views.suggest, name="suggest"),
    re_path(r'^delete$', views.delete, name="delete"),
    re_path(r'^restore$', views.restore, name="restore"),
    re_path(r'^rename/(?P<tag>.*)$', views.rename, name="rename"),
    re_path(r'^pin/(?P<tag>.*)$', views.pin, name="pin"),
    re_path(r'^htmlBlock/(?P<tag>\d+)$', views.htmlBlock, name="htmlBlock"),
    re_path(r'^tag$', views.tag, name="tag"),
    re_path(r'^untag$', views.untag, name="untag"),
    re_path(r'^~(?P<tag>.*)$', views.filter, name="filter"),
    re_path(r'^untagged$', views.untagged, name="untagged"),
]
