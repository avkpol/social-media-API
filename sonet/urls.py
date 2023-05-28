from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sonet.views import (
    PostViewSet,
    CreatePostView,
    RetrieveOwnPostsView,
    RetrieveFollowingPostsView,
    RetrievePostsByHashtagView, LikePostView, LikedPostsView,

)
from user.views import MyPostsView

router = DefaultRouter()
router.register(r"post", PostViewSet, basename="post")

urlpatterns = [
    path('me/', MyPostsView.as_view(), name='my-posts'),
    path("create/", CreatePostView.as_view(), name="create_post"),
    path("own/", RetrieveOwnPostsView.as_view(), name="own_posts"),
    path("following/", RetrieveFollowingPostsView.as_view(), name="following_posts"),
    path("by_hashtag/", RetrievePostsByHashtagView.as_view(), name="posts_by_hashtag"),
    path("api/", include(router.urls)),
    path('post/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('user/liked_posts/', LikedPostsView.as_view(), name='liked-posts'),
]

app_name = "sonet"
