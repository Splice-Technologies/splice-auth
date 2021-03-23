from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateUserSerializer, UserSerializer, ConfirmUserSerializer, ConfirmPasswordResetSerializer
from ..services import UserService


class CreateUserView(APIView):
    def post(self, request):
        create_user_serializer = CreateUserSerializer(data=request.data)

        if create_user_serializer.is_valid(raise_exception=True):
            username = create_user_serializer.validated_data['username']
            password = create_user_serializer.validated_data['password']
            email = create_user_serializer.validated_data['email']

            user = UserService.create_user(username, email, password)
            user_serializer = UserSerializer(instance=user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class ConfirmUserView(APIView):
    def get(self, request):
        confirm_user_serializer = ConfirmUserSerializer(data=request.query_params)

        if confirm_user_serializer.is_valid(raise_exception=True):
            confirmation_code = confirm_user_serializer.validated_data['confirmation_code']
            confirmation = UserService.confirm_user(confirmation_code)

            return Response(confirmation, status=status.HTTP_200_OK)

    def post(self, request):
        confirm_user_serializer = ConfirmUserSerializer(data=request.data)

        if confirm_user_serializer.is_valid(raise_exception=True):
            confirmation_code = confirm_user_serializer.validated_data['confirmation_code']
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
        confirm_password_reset_serializer = ConfirmPasswordResetSerializer(data=request.data)

        if confirm_password_reset_serializer.is_valid(raise_exception=True):
            password = confirm_password_reset_serializer['password']
            password_reset_code = confirm_password_reset_serializer['password_reset_code']
            confirmation = UserService.confirm_password_reset(password, password_reset_code)

            return Response(confirmation, status=status.HTTP_200_OK)
