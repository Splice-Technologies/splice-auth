from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .serializers import (CreateUserSerializer,
                          UserSerializer,
                          ConfirmUserSerializer,
                          ConfirmPasswordResetSerializer,
                          UpdateUserSerializer,
                          ConfirmEmailResetSerializer)
from ..services import UsersService
from ..utils import UsersUtils


class CreateUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')

            user = UsersService.create_user(username, email, password)
            user_serializer = UserSerializer(instance=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class ConfirmUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ConfirmUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            confirmation_code = serializer.validated_data.get('confirmation_code')
            confirmation = UsersService.confirm_user(confirmation_code)

            return UsersUtils.generate_message_response('Your user was successfully activated.', success=confirmation)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        UsersService.reset_password(request.user)

        return UsersUtils.generate_message_response('Password reset code was sent to your email.')


class ConfirmPasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ConfirmPasswordResetSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            password_reset_code = serializer.validated_data.get('password_reset_code')
            confirmation = UsersService.confirm_password_reset(request.user, password, password_reset_code)

            return UsersUtils.generate_message_response('Your password was successfully changed.', success=confirmation)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request) -> Response:
        serializer = UpdateUserSerializer(data=request.data, instance=request.user, partial=True)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username', request.user.username)
            first_name = serializer.validated_data.get('first_name', request.user.first_name)
            last_name = serializer.validated_data.get('last_name', request.user.last_name)

            user = UsersService.update_user(request.user, username, first_name, last_name)
            user_serializer = UserSerializer(instance=user)

            return Response(user_serializer.data, status=status.HTTP_200_OK)


class ResetEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        UsersService.reset_email(request.user)

        return UsersUtils.generate_message_response('Email reset code was sent to your email.')


class ConfirmEmailResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ConfirmEmailResetSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            email_reset_code = serializer.validated_data.get('email_reset_code')
            confirmation = UsersService.confirm_email_reset(email, email_reset_code)

            return UsersUtils.generate_message_response('User confirmation code was sent to your email.',
                                                        success=confirmation)
