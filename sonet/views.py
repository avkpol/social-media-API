from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import Follower
from .models import Post
from .serializers import PostSerializer


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

#
# class FollowerViewSet(viewsets.ModelViewSet):
#     queryset = Follower.objects.all()
#     serializer_class = FollowerSerializer
#
#     @action(detail=False, methods=["get"])
#     def followers(self, request, username=None):
#         user = request.user
#         followers = self.queryset.filter(followed_user__username=username)
#         serializer = self.get_serializer(followers, many=True)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=["get"])
#     def following(self, request, username=None):
#         user = request.user
#         following = self.queryset.filter(user__username=username)
#         serializer = self.get_serializer(following, many=True)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=["post"])
#     def follow(self, request, username=None):
#         user = request.user
#         serializer = FollowerCreateSerializer(
#             data={"user": user.id, "followed_user": username}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     @action(detail=False, methods=["delete"])
#     def unfollow(self, request, username=None):
#         user = request.user
#         follower = self.queryset.get(user=user, followed_user__username=username)
#         follower.delete()
#         return Response(status=204)
