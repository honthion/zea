"""tutorial URL Configuration

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
import monitor.my_scheduler.wechat  # NOQA @isort:skip
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'items', monitor_views.ItemViewSet)
router.register(r'records', monitor_views.RecordViewSet)
router.register(r'users', monitor_views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^monitor/', include(monitor_urls)),

    url(r'^register$', monitor_views.register),
    url(r'^login_out$', monitor_views.logout_view),
    url(r'^login$', monitor_views.login_index),
    url(r'^index$', monitor_views.index),
    url(r'^welcome$', monitor_views.welcome, name='welcome'),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^admin/', include(admin.site.urls)),
]

import logging
logging.debug("debug")