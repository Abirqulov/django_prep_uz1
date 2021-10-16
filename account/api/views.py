# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from .serializers import RegistrationSerializer, LoginSerializer
#
#
# class RegistrationAPIView(APIView):
#     """
#     Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer
#
#     def post(self, request):
#         user = request.data.get('user', {})
#
#         # Паттерн создания сериализатора, валидации и сохранения - довольно
#         # стандартный, и его можно часто увидеть в реальных проектах.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         user = request.data.get('user', {})
#
#         # Обратите внимание, что мы не вызываем метод save() сериализатора, как
#         # делали это для регистрации. Дело в том, что в данном случае нам
#         # нечего сохранять. Вместо этого, метод validate() делает все нужное.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# #
from .serializers import *
from ..models import *
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework import response, status
from django.contrib.auth import authenticate


class UsersView(GenericAPIView):
    serializer_class = RegisterSerializers
    queryset = User.objects.all()


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request):
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

