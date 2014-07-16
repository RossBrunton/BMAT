from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r"^$", "users.views.home", name="home"),
    url(r"^import$", "users.views.importFile", name="import"),
    
    url(r"^logout$", "users.views.logout", name="logout"),
    url(r"^login$", "users.views.login", name="login"),
    url(r"^register$", "users.views.register", name="register"),
)
