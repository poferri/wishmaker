from django.conf.urls import url
from . import views  # This line is new!


urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^add/$", views.add, name="add"),
    url(r"^create/$", views.create, name="create"),
    url(r"^edit/(?P<wish_id>\d+)/$", views.edit, name="edit"),
    url(r"^update/(?P<wish_id>\d+)/$", views.update, name="update"),
    url(r"^delete/(?P<wish_id>\d+)/$", views.delete, name="delete"),
    url(r"^like/(?P<wish_id>\d+)/$", views.like, name="like"),
    url(r"^unlike/(?P<wish_id>\d+)/$", views.unlike, name="unlike"),
    url(r"^viewstats/$", views.viewstats, name="viewstats"),
    url(r"^grant/(?P<wish_id>\d+)/$", views.grant, name="grant"),
    url(r"^home/$", views.home, name="home"),
    url(r"^about/$", views.about, name="about"),
    url(r"^python/$", views.python, name="python"),
    url(r"^csharp/$", views.csharp, name="csharp"),
    url(r"^contact/$", views.contact, name="contact"),

]
