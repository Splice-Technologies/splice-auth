from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .serializers import (PublicUserSerializer,
                          CreateUserSerializer,
                          SelfUserSerializer,
                          UserSerializer,
                          ConfirmUserSerializer,
                          ConfirmPasswordResetSerializer,
                          UpdateUserSerializer,
                          ConfirmEmailResetSerializer,
                          ConfirmUserDeleteSerializer)
from ..services import UsersService
from ..utils import UsersUtils


class ListUserView(APIView):
    def get(self, request: Request) -> Response:
        users = UsersService.list_users()
        serializer = PublicUserSerializer(instance=users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailUserView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        user = UsersService.get_user(pk)
        serializer = PublicUserSerializer(instance=user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SelfUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        serializer = SelfUserSerializer(instance=user)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
            confirmation = UsersService.confirm_email_reset(request.user, email, email_reset_code)

            return UsersUtils.generate_message_response('User confirmation code was sent to your email.',
                                                        success=confirmation)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        UsersService.delete_user(request.user)

        return UsersUtils.generate_message_response('User delete code was sent to your email.')


class ConfirmUserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ConfirmUserDeleteSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_delete_code = serializer.validated_data.get('user_delete_code')
            confirmation = UsersService.confirm_user_delete(request.user, user_delete_code)

            return Response(confirmation, status=status.HTTP_204_NO_CONTENT)


