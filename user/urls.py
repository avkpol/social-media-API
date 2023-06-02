from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    ManageUserView,
    UserSearchView,
    UserLoginView,
    UserLogoutView,
    UserProfileListAPIView,
    UserProfileUpdateDeleteView,
    UserDetailView,
    FollowingUserListAPIView,
    user_endpoints,
    FollowerListView,
)


urlpatterns = [
    path("endpoints/", user_endpoints, name="user-endpoints"),
    path("user/login/", UserLoginView.as_view(), name="user_login"),
    path("user/logout/", UserLogoutView.as_view(), name="user_logout"),
    path("user/register/", CreateUserView.as_view(), name="create"),
    path("user/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/me/", ManageUserView.as_view(), name="me"),
    path("user/users/search/", UserSearchView.as_view(), name="user-search"),
    path(
        "user/profiles/<int:pk>/",
        UserProfileUpdateDeleteView.as_view(),
        name="profile-update",
    ),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-details"),
    path("user/all/", UserProfileListAPIView.as_view(), name="user-list"),
    path("user/following/", FollowingUserListAPIView.as_view(), name="user_following"),
    path("user/<int:pk>/followers/", FollowerListView.as_view(), name="follower-list"),

]

app_name = "user"
