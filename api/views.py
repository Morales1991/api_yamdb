import secrets

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from library.models import Category, Genre, Title, Review, Comment
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer,
                          UserSerializer)
from .permissions import IsAdminOrReadOnly, IsAdminOrModOrAuthor, IsAdmin
from .filters import TitlesFilter


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    ordering = ['id']
    lookup_field = 'username'


class MyProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class GetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')

        try:
            user = User.objects.get(email=email, confirmation_code=confirmation_code)
            user.is_active = True
            user.save()
            return Response({'token': user.get_token()})

        except User.DoesNotExist:
            return Response(
                data={'detail': 'Пользователя с такими данными не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            username = serializer.data.get('username')
            confirmation_code = secrets.token_hex(9)
            User.objects.update_or_create(
                defaults={'confirmation_code': confirmation_code},
                email=email, username=username
            )

            send_mail(
                'Registration',
                'Your confirmation code is ' + str(confirmation_code),
                'from@gmail.com',
                [str(email)],
                fail_silently=False,
            )
            return Response({'details': 'Код подтверждения выслан вам на почту'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    ordering = ['id']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    ordering = ['id']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrModOrAuthor]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise ValidationError('Вы уже поставили оценку')

        serializer.save(author=self.request.user, title=title)
        title.update_rating()

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        title.update_rating()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrModOrAuthor]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
