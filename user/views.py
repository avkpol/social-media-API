import json

from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, get_object_or_404, \
    ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer, UserProfileSerializer

from django.contrib.auth.models import User
from rest_framework import generics, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# from user.models import UserProfile
from user.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer


User = get_user_model()



@api_view(['GET'])
def user_endpoints(request):
    base_url = request.build_absolute_uri('/api/user/')
    endpoints = {
        'Login': f"{base_url}login/",
        'Logout': f"{base_url}logout/",
        'Register': f"{base_url}register/",
        'Token': f"{base_url}token/",
        'Refresh Token': f"{base_url}token/refresh/",
        'Verify Token': f"{base_url}token/verify/",
        'Manage User': f"{base_url}me/",
        'Search Users': f"{base_url}users/search/",
        'User Profiles': f"{base_url}profiles/",
        'Update/Delete User Profiles': f"{base_url}profiles/<int:pk>/",
        # 'Create User Profiles': f"{base_url}profiles/create/",
        'Follow User': f"{base_url}follow/<int:pk>/",
        'Unfollow User': f"{base_url}unfollow/<int:pk>/",
        'Following Users': f"{base_url}following/",
        'Users Followers': f"{base_url}followers/",
        'My profiles': f"{base_url}profile/",
        # 'Users Profiles': f"{base_url}profile/<str:username>/",
        'Users Profiles': f"{base_url}all/",
        'Users Profile': f"{base_url}<int:pk>/",

    }
    return Response(endpoints)


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:

                return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh", )

        # Blacklist the refresh token to invalidate it
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"})
        except Exception:
            return Response({"detail": "Invalid token"}, status=401)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user



class UserProfileUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailView(generics.RetrieveAPIView):
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(user, context={'request': request})
        data = serializer.data
        return Response(data)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        request_user = request.user
        if request_user.is_authenticated:
            if user.followers.filter(pk=request_user.pk).exists():
                user.followers.remove(request_user)
                return Response(
                    {
                        "username": user.username,
                        "profile_picture": user.profile_picture.url if user.profile_picture else None,
                        'followed': False
                    }, status=status.HTTP_200_OK
                )
            else:
                user.followers.add(request_user)
                return Response(
                    {
                        "username": user.username,
                        "profile_picture": user.profile_picture.url if user.profile_picture else None,
                        'followed': True
                    },
                    status=status.HTTP_200_OK
                )
        return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileListAPIView(APIView):
    def get(self, request):
        profiles = User.objects.all()
        serializer = UserSerializer(profiles, many=True)
        return Response(serializer.data)



class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class FollowingUserListAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            following_users = request.user.following.all()
            serializer = UserProfileSerializer(following_users, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)