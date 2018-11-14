""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from monitor import views as monitor_views
from monitor import urls as monitor_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
import monitor.my_scheduler.admin_scheduler  # NOQA @isort:skip
# import monitor.my_scheduler.wechat  # NOQA @isort:skip
# Create a router and register our viewsets with it.

from django.views import static
from django.conf import settings

router = DefaultRouter()
router.register(r'items', monitor_views.ItemViewSet)
router.register(r'records', monitor_views.RecordViewSet)
router.register(r'users', monitor_views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^rauma/monitor/', include(monitor_urls)),

    url(r'^rauma/register$', monitor_views.register),
    url(r'^rauma/login_out$', monitor_views.logout_view),
    url(r'^rauma/login$', monitor_views.login_index),
    url(r'^rauma/$', monitor_views.login_index),
    url(r'^rauma/index$', monitor_views.index),
    url(r'^rauma/welcome$', monitor_views.welcome, name='welcome'),

    url(r'^rauma/api/', include(router.urls)),
    url(r'^rauma/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rauma/api-token-auth/', obtain_jwt_token),
    url(r'^rauma/admin/', include(admin.site.urls)),

    url(r'^rauma/static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')
]

handler404 = monitor_views.page_not_found

import logging
logging.debug("debug")