import re
from django.core.exceptions import ValidationError
import random
from datetime import timedelta, datetime
number_codes = ('99', '98', '97', '95', '94', '93', '91', '90', '77', '55', '33', '71')


def username_validation(username):
    pattern = r'^998(' + '|'.join(number_codes) + r')\d{7}$'
    if re.match(pattern, username):
        return True
    raise ValidationError('Username should be an Uzbek phone number')


def otp_code_generator():
    return random.randint(10000, 99999)


def otp_code_expire(created_at):
    if datetime.now() - created_at > timedelta(minutes=3):
        return False
    return True
