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

from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r'^$', "tags.views.home", name="home"),
    
    url(r'^suggest/(?P<value>.*)$', "tags.views.suggest", name="suggest"),
    url(r'^delete$', "tags.views.delete", name="delete"),
    url(r'^restore$', "tags.views.restore", name="restore"),
    url(r'^rename/(?P<tag>.*)$', "tags.views.rename", name="rename"),
    url(r'^pin/(?P<tag>.*)$', "tags.views.pin", name="pin"),
    url(r'^htmlBlock/(?P<tag>\d+)$', "tags.views.htmlBlock", name="htmlBlock"),
    url(r'^tag$', "tags.views.tag", name="tag"),
    url(r'^untag$', "tags.views.untag", name="untag"),
    url(r'^~(?P<tag>.*)$', "tags.views.filter", name="filter"),
    url(r'^untagged$', "tags.views.untagged", name="untagged"),
)
