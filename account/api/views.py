from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework import response, status
from .serializers import *
from .renderers import *
from django.contrib.auth import authenticate
from rest_framework import generics


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request):
        # user = request.data.get('user', {})
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request):
        print(('request.data', request.data))
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'messeges': 'Login yoki parol mos kelmadi!'}, status=status.HTTP_401_UNAUTHORIZED)


class RegionListView(generics.ListAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class RegionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


# class UserProfileApiView(GenericAPIView):
#     serializer_class = UserProfileSerializer
#
#     def post(self, request):
#         # user = request.data.get('user', {})
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_201_CREATED)
#         return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

