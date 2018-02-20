from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.roads_list, name='roads_list'),
    url(r'^(?P<road_code>[0-9]+)/$', views.get_road, name='road_at_code'),
    url(r'^(?P<road_code>[0-9]+)/of_azs/$', views.get_azs, name='road_of_azs'),
]