from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.views import View
from django.contrib.auth import authenticate, login

from interface.forms import UserRegisterForm, UserUpdateForm, SmsCodeForm
from users.models import User
from users.services import create_unique_invite_code, generate_sms_code


class UserCreateView(CreateView):
    """Сохраняет пользователя при первой регистрации (отправляет код для входа), и присвает инвайт-кож при первом входе"""

    template_name = "interface/register.html"
    model = User
    form_class = UserRegisterForm  # Форма для регистрации
    success_url = reverse_lazy("interface:login")  # URL для перенаправления

    def get_success_url(self):
        # Создает URL для работы с кодом, добавляя номер телефона в параметры
        return reverse_lazy("interface:sms_code") + "?phone=" + self.object.phone

    def form_valid(self, form, *args, **kwargs):
        return_data = {}

        form.is_valid()
        user = form.save()  # Сохраняет пользователя из валидной формы
        user.invite_code = (
            create_unique_invite_code()
        )  # Генерирует и присваивает инвайт-код
        return_data["invite_code"] = user.invite_code

        password = generate_sms_code()  # Генерирует временный пароль
        user.set_password(password)  # Устанавливает сгенерированный пароль

        # Отправляет временный SMS-код
        user.save()  # Сохраняет изменения в пользователе

        return super().form_valid(form)  # Переходит к следующему шагу

    def form_invalid(self, form, *args, **kwargs):
        # Если форма невалидная, пытаемся получить уже существующего пользователя
        user = User.objects.get(phone=form.data.get("phone"))

        password = generate_sms_code()  # Генерирует новый пароль
        user.set_password(password)  # Устанавливает новый пароль

        user.save()  # Сохраняет пользователя

        self.object = user  # Обновляет объект пользователя
        return redirect(self.get_success_url())  # Переходит к следующему шагу


class SmsCodeView(View):
    """Проверка SMS-кода и авторизации пользователя"""

    def post(self, *args, **kwargs):
        phone = self.request.POST.get(
            "phone"
        )  # Получаем номер телефона из POST-запроса
        code = self.request.POST.get("code")  # Получаем код из POST-запроса
        user = authenticate(
            self.request, username=phone, password=code
        )  # Проверяем пользователя
        if user is not None:
            login(
                self.request, user
            )  # Если пользователь аутентифицирован, выполняем вход
            # Перенаправляем на страницу с успехом после логина
            return redirect(reverse("interface:user_detail"))
        else:
            # Если аутентификация не прошла, перенаправляем на страницу логина
            return redirect(reverse("interface:login"))

    def get(self, *args, **kwargs):
        form = SmsCodeForm()  # Создает экземпляр формы для ввода кода
        return render(
            self.request, "interface/sms_code.html", {"form": form}
        )  # Отображает форму


class UserDetailView(DetailView):
    """Отображение данных пользователя"""

    model = User  # Отображение данных
    template_name = (
        "interface/user_detail.html"  # Шаблон для показа деталей пользователя
    )

    def get_object(self, queryset=None):
        # Получает текущего пользователя из запроса
        return self.request.user


class UserUpdateView(UpdateView):
    """Обновление данных пользователя"""

    model = User  # Модель для обновления данных
    template_name = "interface/user_form.html"  # Шаблон для формы обновления
    form_class = UserUpdateForm  # Форма для обновления данных пользователя
    success_url = reverse_lazy(
        "interface:user_detail"
    )  # URL для перенаправления после успешного обновления

    def get_object(self, queryset=None):
        # Получает новые данные для обновления пользователя
        return self.request.user

    def get_success_url(self):
        # Формирует URL для перенаправления, добавлет номер телефона в параметры запроса
        return reverse_lazy("interface:user_detail") + "?phone=" + self.object.phone