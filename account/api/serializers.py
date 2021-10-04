from rest_framework import serializers
from ..models import *


class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class UserLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')