from rest_framework import serializers
from .models import User, Region
# from django.contrib.auth import get_user_model
#
# User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password == password2:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error': 'Both passwords do not match'
            })


class RegionSerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'childs', 'slug']

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('id')
        request = self.context.get('request')
        return RegionSerializer(childs, many=True, context={'request': request}).data


class RegionParentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'slug']


class UserProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'image', 'region',
                  'birth_date', 'gender', 'user_about']

        def to_representation(self, instance):
            self.fields['region'] = RegionSerializer(read_only=True)
            return super(UserProfileSerializers, self).to_representation(instance)
