from django.http import HttpRequest

from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from user.models import Follower
from sonet.models import Post, Comment
from sonet.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer
)

from user.urls import user_endpoints
from user.views import User, IsOwnerOrReadOnly


@api_view(["GET"])
def all_endpoints(request):
    http_request = request._request
    user_endpoints_dict = user_endpoints(http_request).data
    post_endpoints_dict = post_endpoints(http_request).data

    endpoints = {
        "User Endpoints": user_endpoints_dict,
        "Sonet Endpoints": post_endpoints_dict,
    }

    return Response(endpoints)


@api_view(["GET"])
def post_endpoints(request):
    base_url = request.build_absolute_uri("/api/sonet/post/")
    endpoints = {
        "Post creation": f"{base_url}create/",
        "My posts": f"{base_url}own/",
        "Retrieve following posts": f"{base_url}following/",
        "Retrieve posts by hashtag": f"{base_url}by_hashtag/",
        "Choose post to like": f"{base_url}<int:post_id>/like/",
        "Liked posts": f"{base_url}user/liked_posts/",
        "Post detail": f"{base_url}<int:post_id>/",
        "Comment the Post": f"{base_url}comment/<int:pk>",
        "All Comments to the Post": f"{base_url}<int:pk>/comment/",
        "Comment update": f"{base_url}comment/<int:pk>/update/",
    }
    return Response(endpoints)


@api_view(["GET"])
def sonet_endpoints(request):
    http_request = HttpRequest()
    http_request.method = request.method
    http_request.META = request.META
    http_request.GET = request.GET
    http_request.POST = request.POST

    user_endpoints_dict = user_endpoints(http_request).data
    post_endpoints_dict = post_endpoints(http_request).data

    endpoints = {
        "User Endpoints": user_endpoints_dict,
        "Sonet Endpoints": post_endpoints_dict,
    }

    return Response(endpoints)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["likes_count"] = instance.likes.count()
        return Response(data)

    @action(detail=False, methods=["get"])
    def followed(self, request):
        user = request.user
        followed_users = (
            Follower.objects.filter(user=user).values_list(
                "followed_user", flat=True
            )
        )
        posts = self.queryset.filter(user__in=followed_users)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def liked_posts(self, request):
        user = request.user
        liked_posts = Post.objects.filter(likes=user)
        serializer = self.get_serializer(liked_posts, many=True)
        return Response(serializer.data)


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
        hashtag = request.query_params.get("hashtag")
        posts = Post.objects.filter(hashtag__name=hashtag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikeMixin:
    def toggle_like(self, post, user):
        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
            return Response(
                {"status": "unliked"}, status=status.HTTP_200_OK
            )
        else:
            post.likes.add(user)
            return Response(
                {"status": "liked"}, status=status.HTTP_200_OK
            )


class LikePostView(LikeMixin, APIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        return self.toggle_like(post, user)


class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["hashtag__name"]

    def perform_create(self, serializer):
        user = self.request.user
        profile, created = User.objects.update_or_create(
            user=user, defaults=serializer.validated_data
        )


class FollowingPostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        queryset = Post.objects.filter(author__in=following_users)

        return queryset


    def post(self, request, *args, **kwargs):
        post_id = kwargs["pk"]
        post = Post.objects.get(pk=post_id)
        user = request.user
        return self.toggle_like(post, user)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post, author=self.request.user)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return Comment.objects.filter(post_id=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
