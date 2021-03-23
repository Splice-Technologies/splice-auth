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
        fields = ['']
