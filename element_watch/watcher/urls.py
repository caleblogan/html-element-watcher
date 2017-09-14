from django.conf.urls import url

from . import views


app_name = 'watcher'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^watched-element/(?P<pk>\d+)/$', views.WatchedElementDetailView.as_view(), name='watched_element_detail'),
    url(r'^watched-element/create/', views.WatchedElementCreateView.as_view(), name='watched_element_create'),
]
