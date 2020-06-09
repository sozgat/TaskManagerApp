from django.urls import path
from django.conf.urls import url
from tasks.views import *

urlpatterns = [

    url(r'^$', task_index),
    url(r'^(?P<id>\d+)/delete', task_delete, name='delete'),
    url(r'^delete2/(?P<id>\d+)', task_delete2, name='delete2'),
    url(r'^create/', task_create, name='task_create'),
    url(r'^stateUpdate/', task_stateUpdate, name='task_stateUpdate'),
]
