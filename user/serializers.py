from django.contrib.auth import get_user_model

from rest_framework import serializers

from user.models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.create(user=user, **validated_data)
        return profile