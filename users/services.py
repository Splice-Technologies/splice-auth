import uuid
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.exceptions import PermissionDenied

from .models import User


class UserService(object):
    @staticmethod
    def create_user(username: str, email: str, password: str) -> settings.AUTH_USER_MODEL:
        user = User.objects.create_user(username, email, password, is_active=False)
        user.email_user(
            'Splice Technologies// Auth - User Confirmation',
            f'http://127.0.0.1:8001/api/users/create/confirm/?confirmation_code={user.confirmation_code}',
            'noreply@splice.com',
            fail_silently=False)

        return user

    @staticmethod
    def confirm_user(confirmation_code: str) -> bool:
        user = get_object_or_404(User, confirmation_code=confirmation_code)
        user.is_active = True
        user.save()

        return True

    @staticmethod
    def get_user_by_username(username: str) -> settings.AUTH_USER_MODEL:
        return get_object_or_404(User, username=username)

    @staticmethod
    def reset_password(user: User) -> None:
        user.password_reset_code = uuid.uuid4().hex
        user.password_reset_expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
        user.save()
        user.email_user(
            'Splice Technologies// Auth - Password Reset',
            f'{user.password_reset_code}',
            'noreply@splice.com',
            fail_silently=False)

    @staticmethod
    def confirm_password_reset(password: str, password_reset_code: str) -> bool:
        user = get_object_or_404(User, password_reset_code=password_reset_code)

        if user.password_reset_expiration < timezone.now():
            raise PermissionDenied()

        user.set_password(password)
        user.save()

        return True
    
    @staticmethod
    def update_user(user: User, username: str, first_name: str, last_name: str) -> settings.AUTH_USER_MODEL:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return user
