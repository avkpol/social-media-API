from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']


# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = UserProfile
#         fields = ["user", 'profile_picture', 'bio']
#
#     def create(self, validated_data):
#         user = self.context['request'].user
#         profile = UserProfile.objects.create(user=user, **validated_data)
#         return profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        # Check if the provided refresh token is valid
        try:
            token = RefreshToken(value)
            token.verify()
            return value
        except Exception:
            raise serializers.ValidationError("Invalid token")


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']