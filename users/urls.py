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

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse, re_path

import users.views as views

app_name="user"
urlpatterns = [
    re_path(r"^$", views.home, name="home"),
    re_path(r"^import$", views.importFile, name="import"),
    re_path(r"^pass_change$", views.pass_change, name="pass_change"),
    re_path(r"^email_change$", views.email_change, name="email_change"),
    re_path(r"^theme_change$", views.theme_change, name="theme_change"),
    
    re_path(r"^logout$", views.logout, name="logout"),
    re_path(r"^login$", views.login, name="login"),
    re_path(r"^register$", views.register, name="register"),

    re_path(r"^preview$", views.preview, name="preview"),

    re_path(r"^make_trial$", views.make_trial, name="make_trial"),
    re_path(r"^upgrade$", views.upgrade, name="upgrade"),

    re_path(r"^reset$", PasswordResetView.as_view(\
        template_name="users/reset.html", success_url="/user/resetDone",\
        email_template_name="users/reset_email.txt"
    )),
    re_path(r"^resetDone$", PasswordResetDoneView.as_view(template_name="users/reset_done.html")),
    re_path(r"^resetConfirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$", PasswordResetConfirmView.as_view(template_name="users/reset_confirm.html",\
        success_url="/user/resetComplete"\
    )),
    re_path(r"^resetComplete$", PasswordResetCompleteView.as_view(template_name="users/reset_complete.html")),
]
