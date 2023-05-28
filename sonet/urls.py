from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sonet.views import PostViewSet, CreatePostView, RetrieveOwnPostsView, RetrieveFollowingPostsView, \
    RetrievePostsByHashtagView, sonet_endpoints, all_endpoints

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')

urlpatterns = [
    path('api/sonet/', all_endpoints, name='all-endpoints'),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('own/', RetrieveOwnPostsView.as_view(), name='own_posts'),
    path('following/', RetrieveFollowingPostsView.as_view(), name='following_posts'),
    path('by_hashtag/', RetrievePostsByHashtagView.as_view(), name='posts_by_hashtag'),
    path('api/', include(router.urls)),
]

app_name = "sonet"
