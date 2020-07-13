from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet,
    CommentViewSet, GetToken, RegistrationView, MyProfile, UserViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/token/', GetToken.as_view(), name='get_token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email/', RegistrationView.as_view()),
    path('users/me/', MyProfile.as_view()),
    path('', include(router.urls)),
]