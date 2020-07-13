from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    class UserRoles:
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

        choices = [
            (USER, USER),
            (MODERATOR, MODERATOR),
            (ADMIN, ADMIN),
        ]

    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    bio = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=9)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_token(self):
        refresh = RefreshToken.for_user(self)
        token = str(refresh.access_token)
        return token
