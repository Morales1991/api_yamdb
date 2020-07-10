from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from .views import Get_token, RegistrationView


urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/token/', Get_token.as_view(), name='get_token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email/', RegistrationView.as_view()),
]