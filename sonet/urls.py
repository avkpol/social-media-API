from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CreatePostView, RetrieveOwnPostsView, RetrieveFollowingPostsView, \
    RetrievePostsByHashtagView

@api_view(['GET'])
def post_endpoints(request):
    base_url = request.build_absolute_uri('/api/post/')
    endpoints = {
        'Login': f"{base_url}login/",

    }
    return Response(endpoints)



urlpatterns = [
    path("", post_endpoints, name="post-endpoints"),
    path('/create/', CreatePostView.as_view(), name='create_post'),
    path('/own/', RetrieveOwnPostsView.as_view(), name='own_posts'),
    path('/following/', RetrieveFollowingPostsView.as_view(), name='following_posts'),
    path('/by_hashtag/', RetrievePostsByHashtagView.as_view(), name='posts_by_hashtag'),
]

app_name = "sonet"
