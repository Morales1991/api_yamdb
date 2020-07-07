from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
