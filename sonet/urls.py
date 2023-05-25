from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, FollowerViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("followers", FollowerViewSet, basename="follower")


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "sonet"
