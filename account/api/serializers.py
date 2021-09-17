from rest_framework import serializers
from ..models import *


class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'birth_date')


class UserLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')