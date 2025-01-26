from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm, forms, CharField, Form

from users.models import User


class UserRegisterForm(ModelForm):
    """Форма для регистрации пользователя."""
    class Meta:
        model = User
        fields = ('phone', )


class UserUpdateForm(UserChangeForm):
    """Обновление данных пользователя."""
    def clean_ref_code(self):
        # Проверяем activated_invite_code
        activated_invite_code = self.cleaned_data.get('activated_invite_code')  # Получаем значение поля activated_invite_code

        # Проверяем, использовался ли уже код
        if self.instance.activated_invite_code:
            raise forms.ValidationError('Код был уже использован')

        # Обрабатываем случаи, когда код не был введен
        if not activated_invite_code:
            return activated_invite_code

        # Проверка на использование собственного кода
        if activated_invite_code == self.instance.invite_code:
            raise forms.ValidationError('Вы не можете использовать собственный же код!')

        # Проверка, на существование указанного кода
        if not User.objects.filter(invite_code=activated_invite_code).exists():
            raise forms.ValidationError('Код не найден!')

        return activated_invite_code  # Возвращаем корректное значение

    class Meta:
        model = User  # Указываем, что эта форма работает с моделью User
        fields = ('name', 'last_name', 'activated_invite_code',)


class SmsCodeForm(Form):
    """Форма для ввода кода из смс."""
    code = CharField(label='Код из СМС')  # Поле для ввода 4-значного кода, отправленного по SMS