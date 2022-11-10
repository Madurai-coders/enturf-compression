from django.urls import include, path
from compression import views


urlpatterns = [
    path('video/', views.livefe, name='video')
]
