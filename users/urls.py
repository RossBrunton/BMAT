from django.conf.urls import patterns, include, url
from django.contrib.auth.views import\
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = patterns("",
    #url(r"^$", "users.views.list", name="list"),
    
    url(r"^logout$", "users.views.logout", name="logout"),
    url(r"^login$", "users.views.login", name="login"),
    url(r"^register$", "users.views.register", name="register"),
    #url(r"^edit$", "users.views.edit", name="edit"),
    #url(r"^official$", "users.views.official", name="official"),
    
    #url(r"^reset$", password_reset,\
    #    {'template_name': "users/reset.html", "post_reset_redirect":"/users/resetDone",\
    #    "email_template_name":"users/reset_email.html"}
    #),
    #url(r"^resetDone$", password_reset_done, {'template_name': "users/reset_done.html"}),
    #url(r"^resetConfirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$", password_reset_confirm,\
    #    {'template_name': "users/reset_confirm.html", "post_reset_redirect":"/users/resetComplete"}\
    #),
    #url(r"^resetComplete$", password_reset_complete, {'template_name': "users/reset_complete.html"}),
)
