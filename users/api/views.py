from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (CreateUserSerializer,
                          UserSerializer,
                          ConfirmUserSerializer,
                          ConfirmPasswordResetSerializer,
                          UpdateUserSerializer, )
from ..services import UserService


class CreateUserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            user = UserService.create_user(username, email, password)
            user_serializer = UserSerializer(instance=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class ConfirmUserView(APIView):
    def get(self, request):
        serializer = ConfirmUserSerializer(data=request.query_params)

        if serializer.is_valid(raise_exception=True):
            confirmation_code = serializer.validated_data['confirmation_code']
            confirmation = UserService.confirm_user(confirmation_code)

            return Response(confirmation, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            confirmation_code = serializer.validated_data['confirmation_code']
            confirmation = UserService.confirm_user(confirmation_code)

            return Response(confirmation, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        UserService.reset_password(request.user)

        return Response({'message': 'Password reset code was sent to your email.'}, status=status.HTTP_200_OK)


class ConfirmPasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConfirmPasswordResetSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data['password']
            password_reset_code = serializer.validated_data['password_reset_code']
            confirmation = UserService.confirm_password_reset(password, password_reset_code)

            return Response(confirmation, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserSerializer(data=request.data, instance=request.user, partial=True)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username', request.user.username)
            first_name = serializer.validated_data.get('first_name', request.user.first_name)
            last_name = serializer.validated_data.get('last_name', request.user.last_name)

            user = UserService.update_user(request.user, username, first_name, last_name)
            user_serializer = UserSerializer(instance=user)

            return Response(user_serializer.data, status=status.HTTP_200_OK)
