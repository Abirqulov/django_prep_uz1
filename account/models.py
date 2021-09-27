from django.db import models
from django.contrib.auth.models import AbstractUser
# from config.constants import GENDER_CHOICES, LANG_CHOICES

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=120)
    birth_date = models.DateField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
