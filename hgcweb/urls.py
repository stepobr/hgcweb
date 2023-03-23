from django.contrib import admin
from django.urls import path, include
from django.conf import settings 

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('base.urls'), name='base'),

]

urlpatterns += staticfiles_urlpatterns()

# admin if enabled in settings
if settings.ADMIN_ENABLED:
    urlpatterns += patterns('',
        (r'^admin/(.*)', include(admin.site.urls)),
    )