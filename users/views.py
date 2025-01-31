from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, ProfileSerializer, SendCodeSerializer, VerifyCodeSerializer, ActivateInviteCodeSerializer

from users.services import send, generate_sms_code, create_unique_invite_code


class SendCodeAPIView(generics.CreateAPIView):
    """ Создает пользователя в БД и отправляет смс по номеру телефона с кодом """
    serializer_class = SendCodeSerializer
    permission_classes = (AllowAny,)



class VerifyCodeAPIView(APIView):
    """ Подтверждение кода, отправленного в смс """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)   # генерируем токены для пользователя
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserProfileRetrieveAPIView(RetrieveAPIView):
    """Обработка отображения данных пользователя"""
    serializer_class = ProfileSerializer  # Указываем сериализатор для отображения профиля
    queryset = User.objects.all()  # Определяем, что будем работать со всеми пользователями
    permission_classes = (IsAuthenticated, IsUser)  # Только аутентифицированные пользователи с правами

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.kwargs['pk'])


class UserUpdateAPIView(UpdateAPIView):
    """Обработка обновления данных пользователя"""
    serializer_class = UserSerializer  # Указываем сериализатор для обработки данных
    queryset = User.objects.all()  # Определяем, что будем работать со всеми пользователями
    permission_classes = (IsAuthenticated, IsUser)  # Только аутентифицированные пользователи с правами

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.kwargs['pk'])


class UserListAPIView(ListAPIView):
    """Обработка списка данных пользоватеей"""
    serializer_class = ProfileSerializer  # Указываем сериализатор для обработки данных
    queryset = User.objects.all()  # Определяем, что будем работать со всеми пользователями
    permission_classes = (IsAuthenticated,)


class ActivateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Активирует инвайт-код.
        """
        serializer = ActivateInviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request.user)
        return Response({"message": "Инвайт-код успешно активирован."}, status=status.HTTP_200_OK)