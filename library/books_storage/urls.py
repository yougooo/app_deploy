from django.conf.urls import url
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^search/$', Search.as_view(), name='search')]

