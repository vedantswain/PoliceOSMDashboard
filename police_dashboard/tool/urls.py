from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/(?P<handle>[^/]+)/$', views.dashboard,name='dashboard'),
    url(r'^graph_comp/$', views.graph_comp, name='graph comparison'),
    url(r'^victimisation_tree/$', views.victimzn_tree, name='victimisation'),
    url(r'^victimisation_actual/$', views.victimzn_actual, name='victimisation actual'),
    url(r'^word_cloud/$', views.word_cloud, name='word cloud'),
]