import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


class User(AbstractUser):
    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    confirmation_code = models.CharField(max_length=36, blank=False, null=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_confirmation_code(sender, instance=None, created=False, **kwargs):
    if created:
        instance.confirmation_code = uuid.uuid4().hex
        instance.save()


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False