from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'media', 'created_at', 'updated_at']

