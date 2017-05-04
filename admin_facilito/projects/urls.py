from django.conf.urls import url

from .views import CreateClass
from .views import ListClass
from .views import ShowClass
from .views import edit
from .views import ListMyProjectsClass
from .views import ListContributorsClass

app_name = 'project'

urlpatterns = [
    
    url(r'^$',ListClass.as_view(), name='projects'),

    url(r'^mine/$',ListMyProjectsClass.as_view(), name='my_projects'),

    url(r'^create/$',CreateClass.as_view(), name='create'),

    url(r'^(?P<slug>[\w-]+)/$',ShowClass.as_view(), name='show'),
    
    url(r'^(?P<slug>[\w-]+)/edit$',edit, name='edit'),

    url(r'^(?P<slug>[\w-]+)/contributors$',ListContributorsClass.as_view(), name='contributors'),

   ]
