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
    # UserProfileCreateView,
    UserProfileListAPIView,
    UserProfileUpdateDeleteView,
    # UserFollowView,
    # UserUnfollowView,
    # UserFollowingListView,
    # UserFollowerListView,
    # UserProfileView,
    # UserProfileDetailView,
    user_endpoints, UserDetailView,
)


urlpatterns = [
    path("endpoints/", user_endpoints, name="user-endpoints"),
    path("user/login/", UserLoginView.as_view(), name="user_login"),
    path("user/logout/", UserLogoutView.as_view(), name="user_logout"),
    path("user/register/", CreateUserView.as_view(), name="create"),
    path("user/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/me/", ManageUserView.as_view(), name="manage"),
    path("user/users/search/", UserSearchView.as_view(), name="user-search"),
    # path(
    #     "user/profiles/create/", UserProfileCreateView.as_view(), name="profile-create"
    # ),
    path(
        "user/profiles/<int:pk>/",
        UserProfileUpdateDeleteView.as_view(),
        name="profile-update",
    ),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-details"),
    path("user/all/", UserProfileListAPIView.as_view(), name='user-list'),
    # path("user/profiles/", UserProfileListAPIView.as_view(), name="profile-list"),
    # path("user/follow/<int:user_pk>/", UserFollowView.as_view(), name="user_follow"),
    # path(
    #     "user/unfollow/<int:user_pk>/", UserUnfollowView.as_view(), name="user_unfollow"
    # ),
    # path("user/following/", UserFollowingListView.as_view(), name="user_following"),
    # path("user/followers/", UserFollowerListView.as_view(), name="user_followers"),
    # path("user/profile/", UserView.as_view(), name="user_profile"),
    # path(
    #     "user/profile/<str:username>/",
    #     UserProfileDetailView.as_view(),
    #     name="user_profile_detail",
    # ),
]


app_name = "user"
