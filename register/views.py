from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, response, generics
from .serializers import UserRegisterSerializer, UserProfileSerializers, RegionSerializer, RegionParentSerializers
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
# from .permissions import IsAuthorOrReadOnly
from .models import User, Region
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutAPIView(APIView):

    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegionApiView(generics.ListAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.filter(parent__isnull=True)


# class RegionSlugApiView(generics.RetrieveAPIView):
#     serializer_class = RegionSerializer
#     queryset = Region.objects.filter(slug__isnull=False)
#
#     def get_object(self):
#         slug = self.kwargs.get('slug')
#         staff = get_object_or_404(Region, slug=slug)
#         return staff


class RegionParentApiView(generics.ListAPIView):
    serializer_class = RegionParentSerializers
    queryset = Region.objects.filter(parent__isnull=True)


class RegionCHildsApiView(generics.ListAPIView):
    serializer_class = RegionParentSerializers
    queryset = Region.objects.filter(parent__isnull=False)


class UserProfileApiView(GenericAPIView):
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated]
    # permission_classes = (IsAuthorOrReadOnly, )

    def post(self, request):
        user_id = self.request.user.id
        singleton_instance = User.objects.get(id=user_id)

        serializer = self.serializer_class(instance=singleton_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

