"""worksite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from otchet.views   import * 

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout), 
    url(r'^accounts/profile/$', profile), 
    url(r'^index/$', index),
    url(r'^otchet/$', list_otchet),
    url(r'^newpost/(\d{1,6})/$', newpost),
    url(r'^delpost/(\d{1,6})/$', delpost),
    url(r'^addpost/$', addpost),
    url(r'^addliftfault/$', addliftfault),
    url(r'^newmail/$', newmail),
    url(r'^$', newpost),
    url(r'^faultcorrect/$', fault_correct),
]
