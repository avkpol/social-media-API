from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, ProfileViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "user"
