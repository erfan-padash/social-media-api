from rest_framework import serializers
from .models import Account, User
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """
    this class made for our custom user class for serialize and deserialize
    """

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password1', 'password2')

    # check if two passwords are match
    def validate(self, data):
        if data['password1'] and data['password2'] and data['password1'] != data['password2']:
            raise ValidationError({
                'password': 'password must be match.'})
        return data


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        exclude = ('user',)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()
