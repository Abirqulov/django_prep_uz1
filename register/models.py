from django.db import models
from django.contrib.auth.models import AbstractUser
from config.constants import *


class Region(models.Model):
    name = models.CharField(max_length=120)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childs', on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=120, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    image = models.ImageField(upload_to='static/user_images', null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(default=None, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50, null=True, blank=True)
    user_about = models.TextField()
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return self.username
