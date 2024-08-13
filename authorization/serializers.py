from rest_framework import serializers
from .models import User, OTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'balance', 'is_verified')


