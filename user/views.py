

from rest_framework import viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'message': 'User registered successfully.', 'user_id': user.id})

    @action(detail=False, methods=['post'])
    def login(self, request):
        # Implement login logic here
        return Response({'message': 'Login successful.'})

    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Implement logout logic here
        return Response({'message': 'Logout successful.'})

    @action(detail=False, methods=['post'])
    def profile(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({'message': 'Profile created successfully.', 'profile_id': profile.id})

    @action(detail=False, methods=['get'])
    def users(self, request):
        query = request.query_params.get('q')
        users = User.objects.filter(username__icontains=query)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

