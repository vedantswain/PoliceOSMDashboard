from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/(?P<handle>[^/]+)/$', views.dashboard,name='dashboard'),
    url(r'^load_name/$', views.load_name, name='load_name'),
]