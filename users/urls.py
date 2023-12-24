""" URLs for user management things

URLs are:
- home
- import
- logout
- login
- register
- preview

And the URLs used by Django's password reset thing:
- reset
- resetDone
- resetConfirm/(code)
- resetComplete
"""

from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse

import users.views as views

app_name="user"
urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^import$", views.importFile, name="import"),
    url(r"^pass_change$", views.pass_change, name="pass_change"),
    url(r"^email_change$", views.email_change, name="email_change"),
    url(r"^theme_change$", views.theme_change, name="theme_change"),
    
    url(r"^logout$", views.logout, name="logout"),
    url(r"^login$", views.login, name="login"),
    url(r"^register$", views.register, name="register"),

    url(r"^preview$", views.preview, name="preview"),

    url(r"^make_trial$", views.make_trial, name="make_trial"),
    url(r"^upgrade$", views.upgrade, name="upgrade"),

    url(r"^reset$", PasswordResetView.as_view(\
        template_name="users/reset.html", success_url="/user/resetDone",\
        email_template_name="users/reset_email.txt"
    )),
    url(r"^resetDone$", PasswordResetDoneView.as_view(template_name="users/reset_done.html")),
    url(r"^resetConfirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$", PasswordResetConfirmView.as_view(template_name="users/reset_confirm.html",\
        success_url="/user/resetComplete"\
    )),
    url(r"^resetComplete$", PasswordResetCompleteView.as_view(template_name="users/reset_complete.html")),
]
