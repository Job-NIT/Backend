from django.db import models
from django.contrib.auth.models import AbstractUser


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
