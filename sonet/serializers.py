from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post, Hashtag, Like


class PostSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=False)
    hashtag = serializers.CharField(max_length=255, write_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'media', 'hashtag', "likes"]

    def create(self, validated_data):
        hashtag_data = validated_data.pop('hashtag', '')
        hashtag_names = [name.strip() for name in hashtag_data.split(',') if name.strip()]
        post = super().create(validated_data)

        for hashtag_name in hashtag_names:
            hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name)
            post.hashtag.add(hashtag)

        return post

    def get_likes(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
