from django.contrib import admin
from django.urls import path, include
from django.conf import settings 

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage' ),
    
    # path('oidc/', include('mozilla_django_oidc.urls')),
    # path('oidc/', include('oauth2_authcodeflow.urls')),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('auth/', views.auth, name='auth'),
    

    path('simodules/', include('simodules.urls')),
    path('scitiles/', include('scitiles.urls')),
    path('cassettes/', include('cassettes.urls')),
    path('logistics/', include('logistics.urls')),
]