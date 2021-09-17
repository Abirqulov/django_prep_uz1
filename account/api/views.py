from .serializers import *
from ..models import *
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework import response, status
from django.contrib.auth import authenticate


class UsersView(GenericAPIView):
    serializer_class = UserRegisterSerializers
    queryset = User.objects.all()


class RegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializers

    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status=status.HTTP_201_CREATED)
        return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializers

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            serializers = self.serializer_class(user)
            return response.Response(serializers.data, status=status.HTTP_200_OK)
        return response.Response({'messages': 'Username yoki parol hato!'}, status=status.HTTP_401_UNAUTHORIZED)

