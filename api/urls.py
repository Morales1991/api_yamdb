from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ReviewViewSet, CommentViewSet, TitleViewSet, CategoryViewSet, GenreViewSet, UserViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'reviews/(?P<review_id>\d+)/comments', CommentViewSet)
router.register(r'users', UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', UserViewSet.as_view({'patch': 'partial_update'})),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
