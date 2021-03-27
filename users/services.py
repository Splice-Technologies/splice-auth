import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.exceptions import PermissionDenied

from .models import User, Email
from .utils import UserUtils
from .conf import UserConf


class UserService(object):
    @staticmethod
    def send_user_confirmation_email(email: str, code: str):
        email_context = {'title': 'User Confirmation', 'code': code}
        email_html = render_to_string('users/confirm_user.html', email_context)
        email_text = strip_tags(email_html)

        email = EmailMultiAlternatives('Splice Technologies// Auth - User Confirmation',
                                       email_text,
                                       'noreply@splice.com',
                                       [email])
        email.attach_alternative(email_html, 'text/html')
        email.send(fail_silently=False)

    @staticmethod
    def create_user(username: str, email: str, password: str) -> settings.AUTH_USER_MODEL:
        user = User.objects.create_user(username, email, password, is_active=False)

        UserService.send_user_confirmation_email(user.email, user.confirmation_code)

        return user

    @staticmethod
    def confirm_user(confirmation_code: str) -> bool:
        user = get_object_or_404(User, confirmation_code=confirmation_code)
        user.is_active = True
        user.save()

        email = Email.objects.get(email=user.email)
        email.validated = True
        email.save()

        return True

    @staticmethod
    def get_user_by_username(username: str) -> settings.AUTH_USER_MODEL:
        return get_object_or_404(User, username=username)

    @staticmethod
    def reset_password(user: User) -> None:
        now = datetime.datetime.now()
        expiration = datetime.timedelta(hours=UserConf.reset_code_expiration)

        user.password_reset_code = UserUtils.generate_uuid4()
        user.password_reset_expiration = now + expiration
        user.save()

        email_context = {'title': 'Password Reset', 'code': user.password_reset_code}
        email_html = render_to_string('users/confirm_password_reset.html', email_context)
        email_text = strip_tags(email_html)

        email = EmailMultiAlternatives('Splice Technologies// Auth - Password Reset',
                                       email_text,
                                       'noreply@splice.com',
                                       [user.email])
        email.attach_alternative(email_html, 'text/html')
        email.send(fail_silently=False)

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

    @staticmethod
    def reset_email(user: User) -> None:
        now = datetime.datetime.now()
        expiration = datetime.timedelta(hours=UserConf.reset_code_expiration)

        user.email_reset_code = UserUtils.generate_uuid4()
        user.email_reset_expiration = now + expiration
        user.save()

        email_context = {'title': 'Email Reset', 'code': user.email_reset_code}
        email_html = render_to_string('users/confirm_email_reset.html', email_context)
        email_text = strip_tags(email_html)

        email = EmailMultiAlternatives('Splice Technologies// Auth - Email Reset',
                                       email_text,
                                       'noreply@splice.com',
                                       [user.email])
        email.attach_alternative(email_html, 'text/html')
        email.send(fail_silently=False)

    @staticmethod
    def confirm_email_reset(email: str, email_reset_code: str) -> bool:
        user = get_object_or_404(User, email_reset_code=email_reset_code)

        if user.email_reset_expiration < timezone.now():
            raise PermissionDenied()

        user.email = email
        user.confirmation_code = UserUtils.generate_uuid4()
        user.is_active = False
        user.save()

        UserService.send_user_confirmation_email(user.email, user.confirmation_code)

        return True
