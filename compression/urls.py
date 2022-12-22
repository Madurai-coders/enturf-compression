from django.urls import include, path,re_path
from compression import views
from . import consumer
from django.urls import re_path as url
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    url('', include(router.urls)),
    # path('video/', views.livefe, name='video'),
    # path('play/', views.index, name='play'),
    # path('new/', views.new, name='new'),
    path('play_vid/', views.hsl, name='play_vid'),
    
    # re_path(r'ws/iot/$', consumer.IotChannelDataConsumer.as_asgi()),
]
