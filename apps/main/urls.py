from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard', views.dashboard),
    url(r'^logout', views.logout),
    url(r'selectCity', views.selectCity),
    url(r'^city/(?P<city_id>\d+)$', views.cityDetail),
    url(r'^processCity', views.processCity),
    url(r'^remove/(?P<city_id>\d+)$', views.removeCity),
    url(r'^processEvent/(?P<city_id>\d+)$', views.processEvent),
    url(r'^remove_event/(?P<event_id>\d+)$', views.removeEvent),
    url(r'^add_user_to_event/(?P<city_id>\d+)$', views.add_user_to_event),
    url(r'^delete_user_from_event/(?P<a_id>\d+)$', views.delete_user_from_event),
    url(r'^error$', views.error)
]