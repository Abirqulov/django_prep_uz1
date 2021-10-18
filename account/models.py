from django.db import models
from django.contrib.auth.models import AbstractUser

from config.constants import GENDER_CHOICES


class Region(models.Model):
    region_name = models.CharField(max_length=155)
    parent = models.ForeignKey('self', related_name='childs', null=True, blank=True, on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.region_name


class User(AbstractUser):
    name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    password = models.CharField(max_length=120, blank=True, null=True)
    # phone = models.CharField(max_length=120, blank=True, null=True)
    # gender = models.CharField(choices=GENDER_CHOICES, max_length=50, null=True, blank=True)
    # birth_date = models.DateField(default=None, null=True, blank=True)
    # user_about = models.TextField()
    # region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


