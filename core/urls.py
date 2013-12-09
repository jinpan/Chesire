from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('chesire.core.views',
    url(r'^$', 'home', name='home'),
    url(r'^wikipedia/$', 'wikipedia', name='wikipedia'),
    url(r'^testing/$', 'testing', name='testing'),

    # url(r'^chesire/', include('chesire.foo.urls')),

)

