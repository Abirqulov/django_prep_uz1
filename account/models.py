from django.db import models
from django.contrib.auth.models import AbstractUser
# from config.constants import GENDER_CHOICES, LANG_CHOICES

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
