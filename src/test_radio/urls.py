from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^v1/', include('test_radio.api.v1.urls', namespace='v1', app_name='api')),
)
