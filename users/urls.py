from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig

from users.views import UserProfileRetrieveAPIView, UserUpdateAPIView, UserListAPIView, \
    SendCodeAPIView, VerifyCodeAPIView, ActivateInviteCodeView

app_name = UsersConfig.name

urlpatterns = [

    path('send_code/', SendCodeAPIView.as_view(), name='send-code'),
    path('verify_code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path("activate_invite_code/", ActivateInviteCodeView.as_view(), name="activate-invite-code"),

    path('users/<int:pk>/', UserProfileRetrieveAPIView.as_view(), name='users_retrieve'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='users_update'),
    path("", UserListAPIView.as_view(), name="user_list"),

    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]