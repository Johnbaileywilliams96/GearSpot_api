from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from GearSpotapi.views import *
from GearSpotapi.models import *
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post'),
router.register(r"users", UserView, "user")

urlpatterns = [
    path('', include(router.urls)), 
]


