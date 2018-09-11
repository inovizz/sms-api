"""Urls file defining routers for app - api."""
from django.conf.urls import url, include
from rest_framework import routers
from . import views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'users', views.UserViewSet)
ROUTER.register(r'inbound/sms', views.InBoundViewSet)
ROUTER.register(r'outbound/sms', views.OutBoundViewSet)

urlpatterns = [
    url(r'^', include(ROUTER.urls)),
]

app_name = 'api'
