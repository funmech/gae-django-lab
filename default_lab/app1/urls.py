from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('headers', views.get_headers, name='headers'),
    path('version', views.source_version, name='version'),
    path('envs', views.display_envs, name='envs'),
    path('oauth', views.oauth, name='oauth'),
    path('redirect_url', views.oauth_redirect, name='oauth_redirect_url')
]
