from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication


from django.contrib.auth.models import User
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated

from user.models import Profile
from user.serializers import UserSerializer, ProfileSerializer



User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.all()
