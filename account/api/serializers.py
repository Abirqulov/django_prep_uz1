from rest_framework import serializers
from ..models import *
from django.contrib.auth import authenticate


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username',  'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')
