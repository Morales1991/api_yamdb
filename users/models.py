from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomSuperUser(BaseUserManager):
    ##переопределяем
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    ##это тоже переопрелеляем
    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    confirmation_code = models.CharField(max_length=8, default='12345678')
    bio = models.TextField(max_length=1000, blank=True)

    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(max_length=9, choices=USER_ROLES, default='user')

    objects = CustomSuperUser()