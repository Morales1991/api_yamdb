from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from rest_framework_simplejwt.tokens import RefreshToken


class MyUserManager(BaseUserManager):
    def create_superuser(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.create_user(
            email=email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

def get_tokens(self):
    refresh = RefreshToken.for_user(self)
    token = str(refresh.access_token)
    return token
