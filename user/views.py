from django.contrib.auth import get_user_model, authenticate

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer



from django.contrib.auth.models import User
from rest_framework import generics, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserProfile
from user.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, UserProfileSerializer, \
    FollowingSerializer, FollowerSerializer

User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # Assign the profile to the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
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
# class UserProfileRetrieveAPIView(APIView):
#     def get(self, request, profile_id):
#         profile = UserProfile.objects.get(pk=profile_id)
#         serializer = UserProfileSerializer(profile)
#         return Response(serializer.data)

class UserProfileListAPIView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class UserSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', )
        users = []
        if query:
            users = User.objects.filter(username__icontains=query)
            # Add additional filtering criteria if needed
            # For example: users = User.objects.filter(email__icontains=query)
        serializer = UserSerializer(users, many=True)
        response_data = {
            'query': query,
            'results': serializer.data
        }
        return Response(response_data)



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
        refresh_token = request.data.get("refresh", )

        # Blacklist the refresh token to invalidate it
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"})
        except Exception:
            return Response({"detail": "Invalid token"}, status=401)

class UserFollowView(APIView):
    serializer_class = UserProfileSerializer

    def post(self, request, user_pk):
        user = request.user
        try:
            target_user = get_object_or_404(User, id=user_pk)
            user.follow(target_user)
            serializer = FollowingSerializer(target_user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)


class UserUnfollowView(APIView):
    serializer_class = UserProfileSerializer

    def post(self, request, user_pk):
        user = request.user
        try:
            target_user = User.objects.get()
            user.unfollow(target_user)
            return Response({'detail': 'User unfollowed successfully.'})
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

class UserFollowingListView(APIView):
    def get(self, request):
        user = request.user
        following = user.get_following()
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data)

class UserFollowerListView(APIView):
    def get(self, request):
        user = request.user
        followers = user.get_followers()
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)

class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'

    def get(self, request, username):
        profile = get_object_or_404(UserProfile, user__username=username)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

