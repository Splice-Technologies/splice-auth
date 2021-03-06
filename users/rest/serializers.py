from rest_framework import serializers

from ..models import User


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name']


class SelfUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email']


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


class ConfirmUserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_delete_code']
