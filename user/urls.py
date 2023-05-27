from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.views import (
    CreateUserView,
    ManageUserView,

    UserSearchView, UserLoginView, UserLogoutView, UserProfileCreateView,
    UserProfileListAPIView, UserProfileUpdateDeleteView, UserFollowView, UserUnfollowView, UserFollowingListView,
    UserFollowerListView,
)

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
        'Create User Profiles': f"{base_url}profiles/create/",
        'Follow User': f"{base_url}follow/<int:pk>/",
        'Unfollow User': f"{base_url}unfollow/<int:pk>/",
        'Following Users': f"{base_url}following/",
        'Users Followers': f"{base_url}followers/",

    }
    return Response(endpoints)



urlpatterns = [
    path("", user_endpoints, name="user-endpoints"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("endpoints/", user_endpoints, name="user_endpoints"),
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("users/search/", UserSearchView.as_view(), name="user-search"),

    path('profiles/create/', UserProfileCreateView.as_view(), name='profile-create'),
    path('profiles/<int:pk>/', UserProfileUpdateDeleteView.as_view(), name='profile-update'),
    # path('profiles/<int:profile_id>/retrieve/', UserProfileRetrieveAPIView.as_view(), name='profile-retrieve'),
    path('profiles/', UserProfileListAPIView.as_view(), name='profile-list'),
    path('follow/<int:pk>/', UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:pk>/', UserUnfollowView.as_view(), name='user_unfollow'),
    path('following/', UserFollowingListView.as_view(), name='user_following'),
    path('followers/', UserFollowerListView.as_view(), name='user_followers'),
]



app_name = "user"