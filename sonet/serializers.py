from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=False)

    class Meta:
        model = Post
        fields = ["id", "content", "media"]
