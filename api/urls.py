from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'inbound/sms', views.InBoundViewSet)
router.register(r'outbound/sms', views.OutBoundViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

app_name = 'api'
