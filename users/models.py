from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .utils import UsersUtils


class User(AbstractUser):
    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    confirmation_code = models.CharField(max_length=36, blank=False, null=False)

    password_reset_code = models.CharField(max_length=36, blank=False, null=True)
    password_reset_expiration = models.DateTimeField(blank=True, null=True)

    email_reset_code = models.CharField(max_length=36, blank=False, null=True)
    email_reset_expiration = models.DateTimeField(blank=True, null=True)


class Email(models.Model):
    class Meta:
        verbose_name_plural = 'Emails'
        verbose_name = 'Email'

    email = models.EmailField(blank=False, null=False, unique=True)
    validated = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.email


# noinspection PyUnusedLocal
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_confirmation_code(sender, instance=None, created=False, **kwargs):
    if created:
        instance.confirmation_code = UsersUtils.generate_uuid4()
        instance.save()


# noinspection PyUnusedLocal
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def remember_email(sender, instance=None, created=False, **kwargs):
    if instance is not None:
        Email.objects.get_or_create(email=instance.email)


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
