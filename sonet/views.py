from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from user.models import Follower

from sonet.models import Post
from sonet.serializers import PostSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest


from user.urls import user_endpoints



@api_view(['GET'])
def all_endpoints(request):
    http_request = request._request  # Get the original HttpRequest object
    user_endpoints_dict = user_endpoints(http_request).data
    post_endpoints_dict = post_endpoints(http_request).data

    endpoints = {
        'User Endpoints': user_endpoints_dict,
        'Sonet Endpoints': post_endpoints_dict,
    }

    return Response(endpoints)

@api_view(['GET'])
def post_endpoints(request):
    base_url = request.build_absolute_uri('/api/sonet/post/')
    endpoints = {
        'Post creation': f"{base_url}create/",
        'Retrieve own posts': f"{base_url}own/",
        'Retrieve following posts': f"{base_url}following/",
        'Retrieve posts by hashtag': f"{base_url}by_hashtag/",
    }
    return Response(endpoints)



@api_view(['GET'])
def sonet_endpoints(request):
    http_request = HttpRequest()
    http_request.method = request.method
    http_request.META = request.META
    http_request.GET = request.GET
    http_request.POST = request.POST

    user_endpoints_dict = user_endpoints(http_request).data
    post_endpoints_dict = post_endpoints(http_request).data

    endpoints = {
        'User Endpoints': user_endpoints_dict,
        'Sonet Endpoints': post_endpoints_dict,
    }

    return Response(endpoints)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=["get"])
    def followed(self, request):
        user = request.user
        followed_users = Follower.objects.filter(user=user).values_list(
            "followed_user", flat=True
        )
        posts = self.queryset.filter(user__in=followed_users)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)



class CreatePostView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RetrieveOwnPostsView(APIView):
    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class RetrieveFollowingPostsView(APIView):
    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(user__in=following_users)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class RetrievePostsByHashtagView(APIView):
    def get(self, request):
        hashtag = request.query_params.get('hashtag')
        posts = Post.objects.filter(hashtags__name=hashtag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
