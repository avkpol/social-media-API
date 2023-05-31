from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        model = get_user_model()
        fields = ["id", "username", "email", "password"]

    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)

    # def update(self):

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = UserProfile
#         # exclude = ('username',)  # Exclude the 'username' field from serialization
#         fields = ('user', 'profile_picture', 'bio')
#
#     def create(self, validated_data):
#         user_profile = UserProfile.objects.get_or_create(user=self.context['request'].user, **validated_data)
#         return user_profile


    # def create(self, validated_data):
    #     # user_profile = UserProfile.objects.get_or_create(user=self.context['request'].user, **validated_data)
    #     return get_user_model().objects.user_profile(**validated_data)




class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.ReadOnlyField(source='user.username')
    # profile_picture = serializers.ReadOnlyField(source='user.profile_picture')

    following = serializers.SerializerMethodField(read_only=True)
    follow = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = User
        fields = ('username', 'profile_picture', 'bio', 'following', 'follow')
        read_only_fields = ('username', 'profile_picture', 'bio', 'following',)

    def get_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user.followers.filter(pk=request.user.pk).exists()
        return False






# class UserProfileSerializer(serializers.Serializer):
#     users = serializers.SerializerMethodField()
#     selected_users = serializers.MultipleChoiceField(choices=[])
#
#     def get_users(self, obj):
#         users = User.objects.all()
#         return [{'id': user.id, 'username': user.username} for user in users]
#
#     def validate_selected_users(self, value):
#         # Perform manual validation for selected users
#         # Check if the selected users exist or meet certain criteria
#         # Raise a validation error if the check fails
#         selected_users = User.objects.filter(id__in=value)
#         if len(selected_users) != len(value):
#             raise serializers.ValidationError("Invalid selected users.")
#         return value
#
#     def create(self, validated_data):
#         selected_users = validated_data.pop('selected_users', [])
#         # Handle creation logic with the selected users
#         pass
#
#     def update(self, instance, validated_data):
#         selected_users = validated_data.pop('selected_users', [])
#         # Handle update logic with the selected users
#         pass



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