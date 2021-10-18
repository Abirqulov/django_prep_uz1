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


class RegionSerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ['id', 'region_name', 'childs']

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('id')
        request = self.context.get('request')
        return RegionSerializer(childs, many=True, context={'request': request}).data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'gender', 'birth_date', 'user_about']