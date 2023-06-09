from django.contrib import admin
from django.urls import path, include
from django.conf import settings 

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.cassettes, name='cassettes'),
    path('construct/', include('cassettes.construct.urls')),
]