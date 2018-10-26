"""geometrica_t URL Configuration

"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('static.urls')),
    url(r'^roads/', include('roads.urls'))
]
