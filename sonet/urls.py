from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sonet.views import (
    PostViewSet,
    CreatePostView,
    RetrieveOwnPostsView,
    RetrieveFollowingPostsView,
    LikePostView,
    LikedPostsView,
    PostSearchView,
    PostDetailView, CommentCreateView, CommentListView, CommentDetailView,
)



router = DefaultRouter()
router.register(r"post", PostViewSet, basename="post")

urlpatterns = [
    # path('me/', MyPostsView.as_view(), name='my-posts'),
    path("api/", include(router.urls)),
    path("create/", CreatePostView.as_view(), name="create_post"),
    path("own/", RetrieveOwnPostsView.as_view(), name="own_posts"),
    path("following/", RetrieveFollowingPostsView.as_view(), name="following_posts"),
    path("by_hashtag/", PostSearchView.as_view(), name="posts_by_hashtag"),
    path("<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("user/liked_posts/", LikedPostsView.as_view(), name="liked-posts"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path('comment/<int:pk>', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/comment/', CommentListView.as_view(), name='all-comments-to-the-post'),
    path('comment/<int:pk>/update/', CommentDetailView.as_view(), name='comment-detail'),
]

app_name = "sonet"
