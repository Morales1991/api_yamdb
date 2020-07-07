from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from library.models import Category, Genre, Title, Review, Comment
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, SendConfirmationCodeSerializer, CheckConfirmationCodeSerializer, UserSerializer, ReviewSerializer, CommentSerializer
from .permissions import IsAdminOrReadOnly, IsAdmin, IsOwnerOrReadOnly, IsAuthorOrAdminOrModerator
from .filters import TitlesFilter
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
import random
from rest_framework.decorators import api_view
from users.models import User
from django.db.models import Avg
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

def generate_confirmation_code():
    randomlist = random.sample(range(0, 9), 8)
    return ''.join([str(x) for x in randomlist])


def send_confirmation_code(request):
    serializer = SendConfirmationCodeSerializer(data=request.data)
    email = request.data.get('email')
    if serializer.is_valid():
        confirmation_code = generate_confirmation_code()
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
        # https://docs.djangoproject.com/en/3.0/topics/auth/passwords/, но можно просто присвоить
        User.objects.filter(email=email).update(
            confirmation_code=make_password(confirmation_code, salt=None, hasher='default'))
        mail_subject = 'Ваш код  подтверждения для Yamdb'
        message = 'Ваш код: {0}'.format(confirmation_code)
        #send_mail(mail_subject, message, 'from@example.com', [email])
        return Response('Ваш код отправлен на {0}'.format(email), status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        # https://docs.djangoproject.com/en/3.0/topics/auth/passwords/ можно просто сравнить, если не шифровалось
        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'неверный код'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# router.register('users', UserViewSet)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]


# path('v1/users/me/', APIUser.as_view()),
class APIUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

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
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise ValidationError('Вы уже поставили оценку')
        serializer.save(author=self.request.user, title=title)
        agg_score = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = agg_score['score__avg']
        title.save(update_fields=['rating'])

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        agg_score = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = agg_score['score__avg']
        title.save(update_fields=['rating'])


    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

