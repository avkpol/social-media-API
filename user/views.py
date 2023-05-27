from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import parser_classes, action
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


from django.contrib.auth.models import User
from rest_framework import generics, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserProfile
from user.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, UserProfileSerializer

User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileCreateAPIView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateAPIView(APIView):
    def put(self, request, profile_id):
        profile = UserProfile.objects.get(pk=profile_id)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        profile = UserProfile.objects.get(pk=profile_id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserProfileRetrieveAPIView(APIView):
    def get(self, request, profile_id):
        profile = UserProfile.objects.get(pk=profile_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class UserProfileListAPIView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.all()

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Generate token or perform login logic

                return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        # Blacklist the refresh token to invalidate it
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"})
        except Exception:
            return Response({"detail": "Invalid token"}, status=401)



