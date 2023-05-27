from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Follower
from . import models
from .models import Post
from .serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
