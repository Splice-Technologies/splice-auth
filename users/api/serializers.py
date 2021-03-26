from rest_framework import serializers

from ..models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ConfirmUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['confirmation_code']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'first_name', 'last_name']


class ConfirmPasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'password_reset_code']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ConfirmEmailResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'email_reset_code']
