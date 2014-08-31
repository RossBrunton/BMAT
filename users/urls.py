from django.conf.urls import patterns, url
from django.contrib.auth.views import\
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.core.urlresolvers import reverse


urlpatterns = patterns("",
    url(r"^$", "users.views.home", name="home"),
    url(r"^import$", "users.views.importFile", name="import"),
    
    url(r"^logout$", "users.views.logout", name="logout"),
    url(r"^login$", "users.views.login", name="login"),
    url(r"^register$", "users.views.register", name="register"),
    
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
)
