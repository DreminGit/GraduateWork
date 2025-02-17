from rest_framework import serializers

from users.models import User
from users.services import send_sms_imitation


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        Генерирует код для пользователя и отправляет его на телефон.
        """
        phone = validated_data["phone"]
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = User.objects.create(phone=phone)

        # Генерируем код и отправляем
        raw_code = user.generate_code()
        # send_sms(phone, raw_code)
        send_sms_imitation(phone, raw_code)
        return user


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        """
        Проверяет email и код.
        """
        phone = data.get("phone")
        code = data.get("code")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким телефоном не найден."
            )

        if user.code != code:
            raise serializers.ValidationError("Код неверный.")

        data["user"] = user
        return data

    def create(self, validated_data):
        """
        Завершает процесс авторизации.
        """
        user = validated_data["user"]
        user.clear_code()  # Убираем код после успешной авторизации
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data.pop("code", None)  # не позволяет обновить четырехзначный код через update
        validated_data.pop("invite_code", validated_data.get("invite_code"))  # не позволяет обновить инвайт-код
        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с доп. информацией о рефералах."""

    invited_users = (
        serializers.SerializerMethodField()
    )  # Создаем поле invited_users, которое генерируется методом

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "name",
            "last_name",
            "invite_code",
            "activated_invite_code",
            "invited_users",
            "code",
            "code_created_at",
            "code_is_active",
        )

    def get_invited_users(self, obj):
        """Метод для получения списка пользователей, которые использовали инвайт-код текущего пользователя."""

        # Фильтруем пользователей, у которых activated_invite_code совпадает с invite_code текущего объекта
        user_list = User.objects.filter(activated_invite_code=obj.invite_code)
        return [user.phone for user in user_list]


class ActivateInviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, invite_code):
        """
        Проверяем существование инвайт-кода в системе.
        """
        if not User.objects.filter(invite_code=invite_code).exists():
            raise serializers.ValidationError("Инвайт-код не существует.")
        return invite_code

    def save(self, user):
        """
        Активируем инвайт-код для текущего пользователя.
        """
        invite_code = self.validated_data["invite_code"]
        if user.activated_invite_code:
            raise serializers.ValidationError("Вы уже активировали инвайт-код.")
        if invite_code == user.invite_code:
            raise serializers.ValidationError(
                "Вы не можете активировать свой инвайт-код"
            )
        user.activated_invite_code = invite_code
        user.save()
        return user
