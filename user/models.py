from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    class USER_TYPE(models.TextChoices):
        FREELANCER = 'Freelancer'
        EMPLOYER = 'Employer'

    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=12, default='')
    user_type = models.CharField(
        max_length=15,
        choices=USER_TYPE.choices,
        default=USER_TYPE.FREELANCER,
        blank=False
    )

    def __str__(self):
        return self.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Employer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    company = models.CharField(max_length=255, blank=True)


class Freelancer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
