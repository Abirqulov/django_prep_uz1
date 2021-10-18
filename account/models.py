from django.db import models
from django.contrib.auth.models import AbstractUser
import jwt

from datetime import datetime, timedelta

from django.conf import settings
# from config.constants import GENDER_CHOICES, LANG_CHOICES


class User(AbstractUser):
    name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    password = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.username

