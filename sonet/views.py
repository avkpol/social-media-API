from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Follower

from sonet.models import Post
from sonet.serializers import PostSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest


from user.urls import user_endpoints
from user.views import User


@api_view(["GET"])
def all_endpoints(request):
    http_request = request._request  # Get the original HttpRequest object
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
        "My posts": f"{base_url}me/",
        "Retrieve own posts": f"{base_url}own/",
        "Retrieve following posts": f"{base_url}following/",
        "Retrieve posts by hashtag": f"{base_url}by_hashtag/",
        "Choose post to like": f"{base_url}<int:post_id>/like/",
        "Liked posts": f"{base_url}user/liked_posts/",

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
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

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
        hashtag = request.query_params.get("hashtag")
        posts = Post.objects.filter(hashtag__name=hashtag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'detail': 'Post liked'}, status=status.HTTP_200_OK)



class LikedPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.liked_posts.all()



# class PostSearchView(generics.ListAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["hashtag__name"]


class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["hashtag__name"]


    def perform_create(self, serializer):
        user = self.request.user
        profile, created = User.objects.update_or_create(user=user, defaults=serializer.validated_data)


class FollowingPostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get the currently authenticated user
        user = self.request.user

        # Get the list of users that the current user is following
        following_users = user.following.all()

        # Filter the posts based on the users being followed
        queryset = Post.objects.filter(author__in=following_users)

        return queryset