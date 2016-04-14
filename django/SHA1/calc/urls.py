from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^success/url/$', views.upload_success, name='success'),
    ]
