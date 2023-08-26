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

from django.conf.urls import url
import tags.views as views

app_name="tags"
urlpatterns = [
    url(r'^$', views.home, name="home"),
    
    url(r'^suggest/(?P<value>.*)$', views.suggest, name="suggest"),
    url(r'^delete$', views.delete, name="delete"),
    url(r'^restore$', views.restore, name="restore"),
    url(r'^rename/(?P<tag>.*)$', views.rename, name="rename"),
    url(r'^pin/(?P<tag>.*)$', views.pin, name="pin"),
    url(r'^htmlBlock/(?P<tag>\d+)$', views.htmlBlock, name="htmlBlock"),
    url(r'^tag$', views.tag, name="tag"),
    url(r'^untag$', views.untag, name="untag"),
    url(r'^~(?P<tag>.*)$', views.filter, name="filter"),
    url(r'^untagged$', views.untagged, name="untagged"),
]
