from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreateUserSerializer, UserSerializer, ConfirmUserSerializer
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
