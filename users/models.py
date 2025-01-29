import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from users.services2 import six_digits_code_generation
from users.validators import phone_validator

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=16, unique=True, verbose_name='Телефон',
                             help_text='Введите номер телефона в формате 79997776655', validators=[phone_validator])
    name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя', **NULLABLE)
    code = models.CharField(verbose_name="код подтверждения", max_length=4, **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', help_text='Введите фамилию', **NULLABLE)
    invite_code = models.CharField(max_length=6, unique=True, verbose_name='Инвайт-код')
    activated_invite_code = models.CharField(max_length=6, verbose_name='Активированный инвайт-код', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone

    def generate_code(self):
        """
        Генерирует 4-значный код, сохраняет его в поле `code'
        """
        raw_code = str(random.randint(1000, 9999))
        self.code = raw_code  # Сохраняем код в поле `code`
        self.save()
        return raw_code  # Возвращаем незашифрованный код

    def clear_code(self):
        """
        Очищает код после успешного применения.
        """
        self.code = None
        self.save()

    def save(self, *args, **kwargs):
        # Генерируем инвайт-код при первом сохранении пользователя
        all_invite_codes = [el.invite_code for el in User.objects.all()]
        if not self.invite_code:
            self.invite_code = six_digits_code_generation(all_invite_codes)
        super().save(*args, **kwargs)