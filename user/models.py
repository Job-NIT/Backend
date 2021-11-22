from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=12, default='')

    def __str__(self):
        return self.username
