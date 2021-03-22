from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .models import User


class UserService(object):
    @staticmethod
    def create_user(username: str, email: str, password: str) -> settings.AUTH_USER_MODEL:
        user = User.objects.create_user(username, email, password, is_active=False)

        subject = 'Splice Technologies Auth User Confirmation'
        message = f'http://127.0.0.1:8001/api/users/create/confirm/?confirmation_code={user.confirmation_code}'
        from_email = 'noreply@localhost'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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
