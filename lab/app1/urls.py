from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('headers', views.get_headers, name='headers'),
    path('version', views.source_version, name='version'),
]
