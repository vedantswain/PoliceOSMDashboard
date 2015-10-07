from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/(?P<handle>[^/]+)/$', views.dashboard,name='dashboard'),
    url(r'^graph1_twitter_comp/$', views.graph1_twitter_comp, name='graph1_twitter_comp'),
]