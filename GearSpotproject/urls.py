from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from GearSpotapi.views import *
from GearSpotapi.models import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post'),
router.register(r"users", UserView, "user"),
router.register(r"comments", CommentView, "comment")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


