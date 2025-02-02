import random
import string


def six_digits_code_generation(existing_invite_codes: list) -> str:
    """Генерация уникального шестизначного кода из букв и цифр"""
    numbers_chars = string.ascii_letters + string.digits
    six_digit_code = "".join(random.choices(numbers_chars, k=6))

    if (
        six_digit_code not in existing_invite_codes
    ):  # проверка инвайт-кода на уникальность
        six_digit_code = six_digit_code
    else:
        while (
            six_digit_code in existing_invite_codes
        ):  # код будет создаваться пока не получится уникальный
            six_digit_code = "".join(random.choices(numbers_chars, k=6))

    return six_digit_code