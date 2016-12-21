from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib import admin
from carls_site.settings import STATIC_URL, config

import home.views as home

urlpatterns = [
    url(r'^$', home.home, name='home'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=STATIC_URL + 'favicon.ico')),
    url(r'^add/$', RedirectView.as_view(url=config.get('Discord', 'add_url')), name='add'),
    url(r'^discord/$', RedirectView.as_view(url=config.get('Discord', 'invite_url')), name='discord'),
    url(r'^github/$', home.github, name='github'),
    url(r'^github/auth/$', home.github_auth, name='github_auth'),
    url(r'^admin/', admin.site.urls, name="django_admin"),
]
