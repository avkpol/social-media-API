from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sonet.views import (
    PostViewSet,
    RetrieveOwnPostsView,
    RetrieveFollowingPostsView,
    LikePostView,
    PostSearchView,
    CommentCreateView,
    CommentListView,
    CommentDetailView,
)


router = DefaultRouter()
router.register(r"post", PostViewSet, basename="post")
router.register(r'create', PostViewSet, basename='create_post')

urlpatterns = [
    path("api/", include(router.urls)),
    path("create/", PostViewSet.as_view(actions={'post': 'create'}), name="create_post"),
    path("own/", RetrieveOwnPostsView.as_view(), name="own_posts"),
    path("following/", RetrieveFollowingPostsView.as_view(), name="following_posts"),
    path("by_hashtag/", PostSearchView.as_view(), name="posts_by_hashtag"),
    path("<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("user/liked_posts/", PostViewSet.as_view(actions={"get": "list"}), name="post-details-like-post"),
    path("<int:pk>/", PostViewSet.as_view(actions={'get': 'retrieve'}), name="post-detail"),
    path("comment/<int:pk>", CommentCreateView.as_view(), name="comment-create"),
    path(
        "<int:pk>/comment/", CommentListView.as_view(), name="all-comments-to-the-post"
    ),
    path(
        "comment/<int:pk>/update/", CommentDetailView.as_view(), name="comment-detail"
    ),
] + router.urls

app_name = "sonet"
