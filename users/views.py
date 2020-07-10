from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import permissions
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer
from .permissions import AdminPermission


User = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username',]
    permission_classes = (permissions.IsAuthenticated,AdminPermission,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,AdminPermission,)
    lookup_field = 'username'


class MyProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
