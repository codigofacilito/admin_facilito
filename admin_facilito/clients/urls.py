from django.conf.urls import url
from . import views

app_name = 'client'

urlpatterns = [
    #url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),
    url(r'^show/(?P<username_url>\w+)/$', views.ShowView.as_view(), name = 'show'),
    url(r'^login/$', views.LoginView.as_view(), name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name = 'dashboard'),
    url(r'^create/$', views.create, name = 'create'),
   ]

