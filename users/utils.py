import uuid

from rest_framework.response import Response
from rest_framework import status


class UsersUtils(object):
    @staticmethod
    def generate_uuid4() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def generate_message_response(message: str, **kwargs) -> Response:
        return Response({'message': message} | kwargs, status=status.HTTP_200_OK)
