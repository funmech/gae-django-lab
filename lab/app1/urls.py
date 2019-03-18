from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('headers', views.headers, name='headers'),
]
