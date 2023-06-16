import datetime as dt
import re

from django.conf import settings
from django.core.exceptions import ValidationError


def symbols_validator(value):
    MESSAGE_SYMBOLS = 'Некорректные символы: {}'
    invalid_simbols = ''.join(set(re.sub(r'([\w.@+-]+)', '', str(value))))
    if invalid_simbols:
        raise ValidationError(MESSAGE_SYMBOLS.format(invalid_simbols))
    return value


def names_validator(value):
    MESSAGE = 'Невозможно использовать {} в качестве имени пользователя.'
    for reserved_username in settings.RESERVED_USERNAMES:
        if value == reserved_username:
            raise ValidationError(MESSAGE.format(value))
    return value


def validate_year(value):
    year = dt.date.today().year
    if not (value <= year):
        raise ValidationError('Некорректный год.')
    return value
