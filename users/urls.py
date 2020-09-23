from django.urls import path

from .api.urls import urlpatterns as api_urlpatterns

app_name = 'users'

urlpatterns = [

] + api_urlpatterns