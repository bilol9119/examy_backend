import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import username_validation, otp_code_generator


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, validators=[username_validation])
    balance = models.IntegerField(default=10)
    password = models.CharField(max_length=200, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class OTP(models.Model):
    otp_key = models.CharField(max_length=300, default=uuid.uuid4)
    otp_code = models.IntegerField(default=otp_code_generator)
    otp_user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)
