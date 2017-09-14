""" URLs for user management things

URLs are:
- home
- import
- logout
- login
- register

And the URLs used by Django's password reset thing:
- reset
- resetDone
- resetConfirm/(code)
- resetComplete
"""

from django.conf.urls import patterns, url
from django.contrib.auth.views import\
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.core.urlresolvers import reverse

import users.views as views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^import$", views.importFile, name="import"),
    url(r"^pass_change$", views.pass_change, name="pass_change"),
    url(r"^email_change$", views.email_change, name="email_change"),
    
    url(r"^logout$", views.logout, name="logout"),
    url(r"^login$", views.login, name="login"),
    url(r"^register$", views.register, name="register"),
    
    url(r"^make_trial$", views.make_trial, name="make_trial"),
    url(r"^upgrade$", views.upgrade, name="upgrade"),
    
    url(r"^reset$", password_reset,\
        {'template_name': "users/reset.html", "post_reset_redirect":"/user/resetDone",\
        "email_template_name":"users/reset_email.txt"},
    name="reset"),
    
    url(r"^resetDone$", password_reset_done, {'template_name': "users/reset_done.html"}, name="resetDone"),
    
    url(r"^resetConfirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$", password_reset_confirm,\
        {'template_name': "users/reset_confirm.html", "post_reset_redirect":"/user/resetComplete"},name="resetConfirm"\
    ),
    
    url(r"^resetComplete$", password_reset_complete, {'template_name': "users/reset_complete.html"},
        name="resetComplete",
    )
]
