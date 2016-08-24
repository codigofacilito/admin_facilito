from django.conf.urls import url

from .views import CreateClass
from .views import ListClass
from .views import ShowClass

app_name = 'project'

urlpatterns = [
    url(r'^create/$',CreateClass.as_view(), name='create'),
    url(r'^show/(?P<slug>[\w-]+)/$',ShowClass.as_view(), name='show'),
    url(r'^my/projects$',ListClass.as_view(), name='my_projects'),
   ]
