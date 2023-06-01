from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User, Follower


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        model = get_user_model()
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.ReadOnlyField(source='user.username')
    # profile_picture = serializers.ReadOnlyField(source='user.profile_picture')

    following = serializers.SerializerMethodField(read_only=True)
    follow = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = User
        fields = ("username", "profile_picture", "bio", "following", "follow")
        read_only_fields = (
            "username",
            "profile_picture",
            "bio",
            "following",
        )

    def get_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.followers.filter(pk=request.user.pk).exists()
        return False


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        try:
            token = RefreshToken(value)
            token.verify()
            return value
        except Exception:
            raise serializers.ValidationError("Invalid token")


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Follower
        fields = ["id", "user", "username", "user_followers"]
