from rest_framework import serializers

from user.serializers import UserSerializer
from sonet.models import Post, Hashtag, Like, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="user.username")
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "user", "content", "created_at"]
        read_only_fields = ["id", "post", "author", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        post_id = self.context["view"].kwargs["pk"]
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=validated_data["content"]
        )
        return comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="user.username")
    like = serializers.BooleanField(write_only=True, default=False)
    likes_count = serializers.SerializerMethodField()
    media = serializers.FileField(required=False)
    comments = CommentSerializer(many=True, read_only=True)
    hashtag = serializers.CharField(max_length=55, required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "media",
            "hashtag",
            "author",
            "user",
            "created_at",
            "updated_at",
            "like",
            "likes_count",
            "comments",
        ]
        read_only_fields = (
            "id", "created_at", "updated_at", "likes_count", "comments"
        )

    def get_hashtag(self, obj):
        return [hashtag.name for hashtag in obj.hashtag.all()]

    def create(self, validated_data):
        hashtag_data = validated_data.pop("hashtag", "")
        hashtag_names = [
            name.strip() for name in hashtag_data.split(",") if name.strip()
        ]
        post = super().create(validated_data)

        for hashtag_name in hashtag_names:
            hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name)
            post.hashtag.add(hashtag)

        return post

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
