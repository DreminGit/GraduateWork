from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig

from users.views import (
    UserProfileRetrieveAPIView,
    UserUpdateAPIView,
    SendCodeAPIView,
    VerifyCodeAPIView,
    ActivateInviteCodeView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", SendCodeAPIView.as_view(), name="login"),
    path("login/verify/", VerifyCodeAPIView.as_view(), name="verify-code"),
    path(
        "activate_invite_code/",
        ActivateInviteCodeView.as_view(),
        name="activate-invite-code",
    ),
    path(
        "profile/<int:pk>/", UserProfileRetrieveAPIView.as_view(), name="user-retrieve"
    ),
    path("profiles/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]