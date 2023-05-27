from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post, Follower


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'media', 'created_at', 'updated_at']


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    followed_user = UserSerializer()

    class Meta:
        model = Follower
        fields = "__all__"


class FollowerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["user", "followed_user"]

