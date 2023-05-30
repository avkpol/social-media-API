from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post, Hashtag, Like


class PostSerializer(serializers.ModelSerializer):
    media = serializers.FileField(required=False)
    # hashtag = serializers.SerializerMethodField()
    hashtag = serializers.CharField(max_length=55, required=False)

    class Meta:
        model = Post
        fields = ['id', 'content', 'media', 'hashtag']

    def get_hashtag(self, obj):
        return [hashtag.name for hashtag in obj.hashtag.all()]

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
