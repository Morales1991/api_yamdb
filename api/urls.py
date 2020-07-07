from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TitleViewSet, CategoryViewSet, GenreViewSet, UserViewSet, APIUser, send_confirmation_code, get_jwt_token, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

router.register('users', UserViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/auth/email/', send_confirmation_code, name='get_token'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/', include(router.urls)),
]
