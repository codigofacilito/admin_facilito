from django.conf.urls import url
from . import views

app_name = 'client'

urlpatterns = [
    url(r'^show/$', views.show, name='show'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^create/$', views.create, name='create'),
]